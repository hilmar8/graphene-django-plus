from rest_framework import throttling


class ThrottleOne(throttling.UserRateThrottle):
    scope = "throttle1"

    def get_rate(self):
        return "1/day"


class ThrottleTwo(throttling.UserRateThrottle):
    scope = "throttle2"

    def get_rate(self):
        return "1/day"


class ThrottleThree(throttling.UserRateThrottle):
    scope = "throttle3"

    def get_rate(self):
        return "1/day"
