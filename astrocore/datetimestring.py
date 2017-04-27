"""
"""
# 10 January 2017
# 10 Jan 2017
# January 10, 2017
# Jan 10, 2017
# 1.10.2017  1-10-2017  1/10/2017  1 10 2017
# 2017.1.10  2017-1-10  2017/1/10  2017 1 10
# 20170110

# 10:45:32.7        # assume 24 hour
# 22:45:32.7        # assume 24 hour
# 10:45:32.7 pm
# 10:45:32.7 p.m.
# 22.759083         # assume 24 hour
# 10 am
# 10 pm

# 2009-06-15T13:45:30
# 20170323T180847


class DateTimeString:
    """
    DateTimeString provides a mechanism to parse date-time strings without needing to specify a format.
    """

    DIGITS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    LETTERS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
    WHITESPACE = (' ', '\t')
    MONTHS = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')
    AMPM = ('am', 'pm')

    def __init__(self, s):
        self.s = None
        self.ls = None
        self.i = None
        self.year = None
        self.month = None
        self.day = None
        self.hours = None
        self.minutes = None
        self.seconds = None
        self.set_datetime(s)

    def get_date_tuple(self):
        if not self.have_date():
            self.parse_datetime()
        if self.have_date():
            return self.year, self.month, self.day
        return None

    def get_datetime_tuple(self, defaultToNoon=False):
        if not self.have_date():
            self.parse_datetime()
        if self.have_date():
            if self.have_time():
                return self.year, self.month, self.day, self.hours, self.minutes, self.seconds
            elif defaultToNoon:
                return self.year, self.month, self.day, 12, 0, 0
            return self.year, self.month, self.day, 0, 0, 0
        return None

    def get_time_tuple(self, defaultToNoon=False):
        if not self.have_date():
            self.parse_datetime()
        if self.have_time():
            return self.hours, self.minutes, self.seconds
        elif defaultToNoon:
            return 12, 0, 0
        return 0, 0, 0

    def have_date(self):
        return not any((self.year is None, self.month is None, self.day is None))

    def have_time(self):
        return not any((self.hours is None, self.minutes is None, self.seconds is None))

    def parse_datetime(self):
        self._skip_whitespace()
        if self._parse_date():
            if not self._parse_t():
                self._skip_whitespace()
            self._parse_time()
    
    def set_datetime(self, s):
        self.s = s.lower()
        self.ls = len(s)
        self.i = 0
        self.year = None
        self.month = None
        self.day = None
        self.hours = None
        self.minutes = None
        self.seconds = None

    def _is_digit(self, c):
        return c in self.DIGITS

    def _is_letter(self, c):
        return c in self.LETTERS

    def _is_whitespace(self, c):
        return c in self.WHITESPACE

    def _parse_am_pm(self):
        i_save = self.i
        err = False
        s = ''
        while self.i < self.ls:
            c = self._parse_character()
            if c == ' ':
                break
            if self._is_letter(c):
                s += c
                self.i += 1
            d = self._parse_delimiter()
            if d is None:
                continue
            if d == '.':
                continue
            err = True
            break
        if not err:
            try:
                i = self.AMPM.index(s)
                if i == 0:
                    if self.hours == 12:
                        self.hours -= 12
                elif i == 1:
                    if self.hours < 12:
                        self.hours += 12
                return True
            except:
                pass
        self.i = i_save
        return False

    def _parse_character(self):
        if self.i < self.ls:
            c = self.s[self.i]
            return c
        return None

    def _parse_date(self):
        parts = []
        while len(parts) < 3:
            n = self._parse_number()
            if n is not None:
                ln = len(n)
                if ln >= 1:
                    if ln <= 5:
                        parts.append((n, ln, '?'))
                    elif ln == 8:
                        parts.append((n[0:4], 4, 'y'))
                        parts.append((n[4:6], 2, 'm'))
                        parts.append((n[6:8], 2, 'd'))
                    elif ln == 9:
                        parts.append((n[0:5], 5, 'y'))
                        parts.append((n[5:7], 2, 'm'))
                        parts.append((n[7:9], 2, 'd'))
                    else:
                        break
            else:
                w = self._parse_word()
                if w is not None:
                    for i, m in enumerate(self.MONTHS):
                        if m.startswith(w):
                            parts.append((i + 1, 0, 'm'))
                            break
                else:
                    break
            if not self._skip_whitespace():
                d = self._parse_delimiter()
                if d is None:
                    continue
                elif d == ',':
                    self._skip_whitespace()
                    continue
        if len(parts) == 3:
            for p in parts:
                if p[1] == 0:
                    if p[2] == 'm':
                        if self.month is not None:
                            self.day = self.month
                        self.month = p[0]
                elif p[1] >= 4:
                    self.year = int(p[0])
                else:
                    v = int(p[0])
                    if (v >= 1) and (v <= 12):
                        if p[2] == '?':
                            if self.month is None:
                                self.month = v
                            elif self.day is None:
                                self.day = v
                            else:
                                pass
                        elif p[2] == 'm':
                            if self.month is None:
                                self.month = v
                            elif self.day is None:
                                self.day = self.month
                                self.month = v
                            else:
                                pass
                        elif p[2] == 'd':
                            if self.day is None:
                                self.day = v
                            else:
                                pass
                    elif v > 12:
                        if self.day is None:
                            self.day = v
                        else:
                            pass
                    else:
                        pass
            return self.have_date()
        return False

    def _parse_delimiter(self):
        c = self._parse_character()
        if c is not None:
            if self._is_letter(c) or self._is_digit(c):
                return None
            self.i += 1
        return c

    def _parse_hours(self):
        n = self._parse_number(True)
        if n is not None:
            ln = len(n[0])
            if ln >= 1:
                if not n[1]:
                    if ln == 6:
                        self.hours = int(n[0][0:2])
                        self.minutes = int(n[0][2:4])
                        self.seconds = int(n[0][4:6])
                        return 4
                    else:
                        self.hours = int(n[0])
                        return 1
                else:
                    v = float(n[0])
                    self.hours = int(v)
                    v = (v - self.hours) * 60.0
                    self.minutes = int(v)
                    v = (v - self.minutes) * 60.0
                    self.seconds = v
                    return 4
        return None

    def _parse_minutes(self):
        n = self._parse_number(True)
        if n is not None:
            ln = len(n[0])
            if ln >= 1:
                if not n[1]:
                    self.minutes = int(n[0])
                    return 2
                else:
                    v = float(n[0])
                    self.minutes = int(v)
                    v = (v - self.minutes) * 60.0
                    self.seconds = v
                    return 3
        self.minutes = 0
        self.seconds = 0
        return 3

    def _parse_number(self, allowDecimal=False):
        i_save = self.i
        have_sign = False
        have_digit = False
        have_decimal = False
        n = ''
        while self.i < self.ls:
            c = self._parse_character()
            if c == '-':
                if have_sign or have_digit:
                    break
                n += c
                have_sign = True
                self.i += 1
                continue
            if self._is_digit(c):
                n += c
                have_digit = True
                self.i += 1
                continue
            if (c == '.') and allowDecimal and not have_decimal:
                n += c
                have_decimal = True
                self.i += 1
                continue
            break
        if have_digit:
            if allowDecimal:
                return n, have_decimal
            return n
        self.i = i_save
        return None

    def _parse_seconds(self):
        n = self._parse_number(True)
        if n is not None:
            ln = len(n[0])
            if ln >= 1:
                self.seconds = float(n[0])
                return 3
        self.seconds = 0
        return 3

    def _parse_t(self):
        c = self._parse_character()
        if c == 't':
            self.i += 1
            return True
        return False

    def _parse_time(self):
        nxt = self._parse_hours()
        if nxt == 1:    # minutes
            self._parse_delimiter()
            nxt = self._parse_minutes()
        if nxt == 2:    # seconds
            self._parse_delimiter()
            nxt = self._parse_seconds()
        if nxt == 3:    # am/pm
            if self.hours > 12:
                nxt = 4
            else:
                self._skip_whitespace()
                self._parse_am_pm()
        if nxt == 4:    # mode
            pass
        return self.have_time()

    def _parse_word(self):
        i_save = self.i
        have_character = False
        w = ''
        while self.i < self.ls:
            c = self._parse_character()
            if self._is_letter(c):
                w += c
                have_character = True
                self.i += 1
                continue
            break
        if have_character:
            return w
        self.i = i_save
        return None

    def _skip_whitespace(self):
        skipped = False
        c = self._parse_character()
        while self._is_whitespace(c):
            skipped = True
            self.i += 1
            c = self._parse_character()
        return skipped
