"""Run the real notebook in temporary folders; never touch the user's database."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.original_cwd = Path.cwd()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(os.chdir, self.original_cwd)
        os.chdir(self.temp.name)
        shutil.copy(ROOT / 'flights.csv', 'flights.csv')
        self.notebook = json.loads((ROOT / 'potter_airlines.ipynb').read_text())
        self.ns = {}
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()
        self.addCleanup(self.capture.__exit__, None, None, None)
        self.run_notebook()
        self.ns['reset_database_to_initial_state']()

    def run_notebook(self):
        for index, cell in enumerate(self.notebook['cells']):
            if cell['cell_type'] == 'code':
                exec(compile(''.join(cell['source']), f'cell_{index}', 'exec'), self.ns)

    def rows(self):
        with sqlite3.connect('potter_airlines.db') as conn:
            return conn.execute('SELECT * FROM flights ORDER BY flight_id').fetchall()

    def seats(self):
        with sqlite3.connect('potter_airlines.db') as conn:
            return conn.execute("SELECT seats_remaining FROM flights WHERE flight_id='PA1002'").fetchone()[0]

    def book(self, answers):
        with patch('builtins.input', side_effect=answers):
            self.ns['run_interactive_booking']()

    def sale(self, count):
        self.ns['simulate_seat_sale'](self.ns['stored_flights'], self.ns['priced_flights'], 'PA1002', count)

    def test_run_all_preserves_booking(self):
        self.book(['YVR', 'PA1002', '2'])
        before = self.rows()
        self.run_notebook()
        self.assertEqual(self.rows(), before)

    def test_repeated_sales_use_current_inventory(self):
        self.sale(10)
        self.sale(10)
        self.assertEqual(self.seats(), 70)

    def test_sale_after_booking_does_not_restore_seats(self):
        self.book(['YVR', 'PA1002', '12'])
        self.sale(10)
        self.assertEqual(self.seats(), 68)

    def test_stale_snapshot_cannot_oversell(self):
        self.book(['YVR', 'PA1002', '89'])
        with self.assertRaises(ValueError):
            self.sale(2)
        self.assertEqual(self.seats(), 1)

    def test_invalid_reset_preserves_all_rows(self):
        self.book(['YVR', 'PA1002', '2'])
        before = self.rows()
        for field, value in [('capacity', 0), ('departure_date', 'bad-date'), ('flight_id', 'PA1001'), ('seats_remaining', 1.5)]:
            with self.subTest(field=field):
                bad = self.ns['flights'].astype(object).copy()
                bad.loc[1, field] = value
                bad.to_csv('bad.csv', index=False)
                with self.assertRaises((ValueError, sqlite3.IntegrityError)):
                    self.ns['reset_database_to_initial_state']('bad.csv')
                self.assertEqual(self.rows(), before)

    def test_insert_failure_rolls_back_reset(self):
        before = self.rows()
        # A real SQLite authorizer rejects insertion after the table was rebuilt.
        connect = sqlite3.connect
        def rejecting_connection(*args, **kwargs):
            conn = connect(*args, **kwargs)
            conn.set_authorizer(lambda action, table, *rest: sqlite3.SQLITE_DENY
                                if action == sqlite3.SQLITE_INSERT and table == 'flights'
                                else sqlite3.SQLITE_OK)
            return conn
        with patch('sqlite3.connect', side_effect=rejecting_connection):
            with self.assertRaises(sqlite3.DatabaseError):
                self.ns['reset_database_to_initial_state']()
        self.assertEqual(self.rows(), before)

    def test_fractional_database_seats_rejected(self):
        for count in [1.5, True, float('nan'), float('inf')]:
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    self.ns['update_db_seats']('PA1002', count)
                self.assertEqual(self.seats(), 90)

    def test_invalid_sale_quantities_rejected(self):
        for count in [0, -1, 1.5, True]:
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    self.sale(count)
                self.assertEqual(self.seats(), 90)

    def test_fractional_class_values_rejected(self):
        for seats, capacity in [(0, 0.5), (1.5, 180), (True, 180)]:
            with self.subTest(seats=seats, capacity=capacity):
                with self.assertRaises(ValueError):
                    self.ns['Flight']('X', 100, seats, capacity, 1, 1, 'A', 'B')
        flight = self.ns['Flight']('X', 100, 90, 180, 1, 1, 'A', 'B')
        with self.assertRaises(ValueError):
            flight.update_seats(-0.5)
        self.assertEqual(flight.seats_remaining, 90)

    def test_invalid_ticket_input_then_valid(self):
        with patch('builtins.input', side_effect=['²', 'abc', '1.5', '0', '-1', '91', '2']):
            self.assertEqual(self.ns['get_ticket_count'](90), 2)

    def test_full_booking_flow_and_repeat(self):
        self.book(['bad', 'YVR', 'BAD', 'YVR', '', 'yvr', 'pa1002', 'abc', '0', '999', '2'])
        self.assertEqual(self.seats(), 88)
        self.book(['YVR', 'PA1002', '3'])
        self.assertEqual(self.seats(), 85)

    def test_last_seats_then_sold_out_selection(self):
        self.book(['YVR', 'PA1002', '90'])
        self.assertEqual(self.seats(), 0)
        self.book(['YVR', 'PA1002', 'EXIT'])
        self.assertEqual(self.seats(), 0)

    def test_exit_and_invalid_db_updates_preserve_data(self):
        before = self.rows()
        self.book(['quit'])
        self.book(['YVR', 'EXIT'])
        for fid, count in [('PA1002', -1), ('PA1002', 181), ('UNKNOWN', 1)]:
            with self.assertRaises(ValueError):
                self.ns['update_db_seats'](fid, count)
        self.assertEqual(self.rows(), before)

    def test_reset_restores_csv(self):
        before = self.rows()
        self.book(['YVR', 'PA1002', '2'])
        self.ns['reset_database_to_initial_state']()
        self.assertEqual(self.rows(), before)

    def test_pricing_and_date_filters(self):
        self.assertEqual([self.ns['get_time_factor'](d) for d in [0, 7, 8, 21, 22]], [1.35, 1.35, 1.1, 1.1, 1])
        priced = self.ns['priced_flights']
        self.assertEqual(len(priced), 18)
        self.assertNotIn('PA1001', priced.flight_id.values)
        self.assertNotIn('PA1007', self.ns['available_flights'].flight_id.values)
        for fid in priced.flight_id:
            self.ns['verify_pricing_consistency'](priced, fid)
        self.assertEqual(float(priced.loc[priced.flight_id == 'PA1002', 'final_price'].iloc[0]), 595.35)


if __name__ == '__main__':
    unittest.main()
