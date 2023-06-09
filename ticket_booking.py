import datetime
import unittest

customer_queue = [
    ("2000-01-01 08:00:00", "P1", 1),
    ("2000-01-01 08:01:00", "P2", 4),
    ("2000-01-01 08:01:40", "P3", 1),
    ("2000-01-01 08:03:00", "P4", 1),
    ("2000-01-01 08:03:00", "P5", 1),
    ("2000-01-01 08:03:30", "P6", 1),
]


class Counter:
    def __init__(self, counter_id, queue_capacity, processing_time):
        self.counter_id = counter_id
        self.queue_capacity = queue_capacity
        self.processing_time = processing_time
        self.queue = []
        self.time_counter_closes = None

    def add_person_to_queue(self, person, ticket_count, current_time):
        self.queue.append((person, current_time, ticket_count))

    def process_tickets(self, current_time, dt):
        processed_at = None
        while self.queue:
            person = self.queue[0][0]
            processed_at = current_time + datetime.timedelta(seconds=self.processing_time)
            print(
                f"Person in the queue: {person} - Enters in the Queue at {dt} and gets ticket at {processed_at}"
            )
            self.queue.pop(0)
        self.time_counter_closes = processed_at
        return processed_at


class TicketBookingCentre:
    def __init__(self, max_counters, queue_capacity, processing_time):
        self.max_counters = max_counters
        self.queue_capacity = queue_capacity
        self.processing_time = processing_time
        self.counters = {}
        self.current_counter_id = 1
        self.current_time = None

    def entry_point(self, p):
        p_entry_time = None
        p_exit_time = None
        while len(customer_queue) > 0:
            person = customer_queue[0][1]
            tickets_to_get = customer_queue[0][2]
            dt = datetime.datetime.strptime(customer_queue[0][0], "%Y-%m-%d %H:%M:%S")
            if person == p and p_entry_time is None:
                p_entry_time = dt
            if self.current_time is None or self.current_time < dt:
                self.current_time = dt
            if not self.counters:
                self.counters[self.current_counter_id] = Counter(
                    self.current_counter_id, self.queue_capacity, self.processing_time
                )

            min_queue_counter = self.get_counter_with_minimum_queue_length()
            if len(min_queue_counter.queue) >= self.queue_capacity:
                self.current_counter_id += 1
                self.counters[self.current_counter_id] = Counter(
                    self.current_counter_id, self.queue_capacity, self.processing_time
                )
                min_queue_counter = self.counters[self.current_counter_id]
            min_queue_counter.add_person_to_queue(person, 1, dt)
            tickets_to_get -= 1
            self.current_time = min_queue_counter.process_tickets(self.current_time, dt)
            count2 = 0
            if tickets_to_get > 0:
                while True:
                    next_person_arrival = datetime.datetime.strptime(
                        customer_queue[count2 + 1][0], "%Y-%m-%d %H:%M:%S"
                    )
                    if next_person_arrival < self.current_time:
                        count2 += 1
                    else:
                        break
                customer_queue.insert(
                    count2 + 1,
                    (
                        datetime.datetime.strftime(
                            self.current_time, "%Y-%m-%d %H:%M:%S"
                        ),
                        person,
                        tickets_to_get,
                    ),
                )
            if person == p and tickets_to_get == 0:
                p_exit_time = self.current_time
            customer_queue.pop(0)
        total_p_time = p_exit_time - p_entry_time
        print(total_p_time)
        return str(total_p_time)

    def get_counter_with_minimum_queue_length(self):
        return min(
            self.counters.values(), key=lambda counter: len(counter.queue)
        )


booking_centre = TicketBookingCentre(
    max_counters=2, queue_capacity=4, processing_time=30
)

