import unittest
import datetime

from temp import TicketBookingCentre


class TicketBookingCentreUnitTest(unittest.TestCase):
    def test_entry_point(self):
        booking_centre = TicketBookingCentre(
            max_counters=2, queue_capacity=4, processing_time=30
        )
        self.assertEqual(booking_centre.max_counters, 2)
        self.assertEqual(booking_centre.queue_capacity, 4)
        self.assertEqual(booking_centre.processing_time, 30)
        total_time = booking_centre.entry_point(p="P2")
        self.assertEqual(total_time, "0:02:30")
