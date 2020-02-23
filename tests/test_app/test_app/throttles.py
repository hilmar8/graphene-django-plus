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


class ThrottleFour(throttling.UserRateThrottle):
    scope = "throttle4"

    def get_rate(self):
        return "1/day"


class ThrottleFive(throttling.UserRateThrottle):
    scope = "throttle5"

    def get_rate(self):
        return "1/day"


class ThrottleSix(throttling.UserRateThrottle):
    scope = "throttle6"

    def get_rate(self):
        return "1/day"


class ThrottleSeven(throttling.UserRateThrottle):
    scope = "throttle7"

    def get_rate(self):
        return "1/day"


class ThrottleEight(throttling.UserRateThrottle):
    scope = "throttle8"

    def get_rate(self):
        return "1/day"


class ThrottleNine(throttling.UserRateThrottle):
    scope = "throttle9"

    def get_rate(self):
        return "1/day"


class ThrottleTen(throttling.UserRateThrottle):
    scope = "throttle10"

    def get_rate(self):
        return "1/day"


class ThrottleEleven(throttling.UserRateThrottle):
    scope = "throttle11"

    def get_rate(self):
        return "1/day"
