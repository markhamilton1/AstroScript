import astrocore.astrodate as ad
import astrocore.datetimestring as dts
import ui


main_view = None
background_color = '#153236'
label_font = ('Menlo', 12)
label_color = '#c7c7c7'
content_font = ('Menlo', 18)
content_color = '#48bd90'
screen_width, screen_height = ui.get_screen_size()


def make_label(x, y, w, h, name=None, text="", style="label", align=ui.ALIGN_LEFT):
    label = ui.Label(frame=(x, y, w, h), text=text)
    label.alignment = align
    label.name = name
    if style == 'label':
        label.font = label_font
        label.text_color = label_color
    elif style == 'content':
        label.font = content_font
        label.text_color = content_color
    return label


def make_switch(x, y, w, h, name=None):
    switch = ui.Switch(frame=(x, y, w, h))
    switch.name = name
    return switch


def make_textfield(x, y, w, h, name=None):
    textfield = ui.TextField(frame=(x, y, w, h))
    textfield.name = name
    return textfield


class AstroDateView(ui.View):

    def __init__(self, width=300):
        self.background_color='clear'
        self.name="datetime_view"
        self.date = ad.AstroDate().alloc_now_utc()
        self.width = width

    def make_astrodate_panel(self):
        x, y, w, h = 0, 0, self.pts(1.0), 21
        date_label = make_label(x, y, w, h, text="Current Date/Time")
        self.add_subview(date_label)
    
        x, y, w, h = 0, y + h, self.pts(1.0), 30
        date_textfield = make_textfield(x, y, w, h, name="date_textfield")
        date_textfield.delegate = self
        date_textfield.text = self.date.get_pretty_string()
        self.add_subview(date_textfield)
    
        x, y, w, h = 0, y + h, self.pts(0.32), 21
        timezone_label = make_label(x, y, w, h, text="Time Zone")
        self.add_subview(timezone_label)
    
        x, y, w, h = x + w + self.pts(0.02), y, self.pts(0.16), h
        daysave_label = make_label(x, y, w, h, text="DS", align=ui.ALIGN_CENTER)
        self.add_subview(daysave_label)
    
        x, y, w, h = x + w + self.pts(0.02), y, self.pts(0.48), h
        longitude_label = make_label(x, y, w, h, text="Longitude")
        self.add_subview(longitude_label)
    
        x, y, w, h = 0, y + h, self.pts(0.32), 30
        timezone_textfield = make_textfield(x, y, w, h, name="timezone_textfield")
        timezone_textfield.delegate = self
        timezone_textfield.text = "%d" % self.date.get_zone_correction()
        self.add_subview(timezone_textfield)
    
        x, y, w, h = x + w + self.pts(0.02), y, self.pts(0.16), h
        daysave_switch = make_switch(x, y, w, h, name="daylight_savings_switch")
        daysave_switch.action = self.switch_changed
        daysave_switch.value = self.date.get_daylight_savings()
        self.add_subview(daysave_switch)
    
        x, y, w, h = x + w + self.pts(0.02), y, self.pts(0.48), h
        longitude_textfield = make_textfield(x, y, w, h, name="longitude_textfield")
        longitude_textfield.delegate = self
        longitude_textfield.text = "%.5f" % self.date.get_longitude()
        self.add_subview(longitude_textfield)
    
        x, y, w, h = self.pts(0.02), y + h + 5, self.pts(0.98), 21
        label = make_label(x, y, w, h, name="lct_label", style="content")
        self.add_subview(label)
    
        x, y, w, h = self.pts(0.02), y + h + 5, self.pts(0.98), 21
        label = make_label(x, y, w, h, name="utc_label", style="content")
        self.add_subview(label)

        x, y, w, h = self.pts(0.07), y + h + 5, self.pts(0.93), 21
        label = make_label(x, y, w, h, name="utc_jd_label", style="content")
        self.add_subview(label)

        x, y, w, h = self.pts(0.02), y + h + 5, self.pts(0.98), 21
        label = make_label(x, y, w, h, name="tdt_label", style="content")
        self.add_subview(label)

        x, y, w, h = self.pts(0.07), y + h + 5, self.pts(0.93), 21
        label = make_label(x, y, w, h, name="tdt_jd_label", style="content")
        self.add_subview(label)
            
        x, y, w, h = self.pts(0.02), y + h + 5, self.pts(0.98), 21
        label = make_label(x, y, w, h, name="gst_label", style="content")
        self.add_subview(label)

        x, y, w, h = self.pts(0.02), y + h + 5, self.pts(0.98), 21
        label = make_label(x, y, w, h, name="lst_label", style="content")
        self.add_subview(label)
                   
        return self.width, y + h

    def set_text_in_label(self, name, text):
        label = self[name]
        if label is not None:
            label.text = text
                
    def pts(self, pct):
        if pct < 0.0:
            return 0.0
        if pct > 1.0:
            pct = 1.0
        return pct * (self.width - 1)

    def update_astrodate_panel(self):
        self.date.to_lct()
        self.set_text_in_label("lct_label", self.date.get_pretty_string())
    
        self.date.to_utc()
        self.set_text_in_label("utc_label", self.date.get_pretty_string())
        self.set_text_in_label("utc_jd_label", "%.6f" % self.date.get_julian())
    
        self.date.to_tdt()
        self.set_text_in_label("tdt_label", self.date.get_pretty_string())
        self.set_text_in_label("tdt_jd_label", "%.6f" % self.date.get_julian())
            
        self.date.to_gst()
        self.set_text_in_label("gst_label", self.date.get_pretty_string())
    
        self.date.to_lst()
        self.set_text_in_label("lst_label", self.date.get_pretty_string())
        
    # Textfield Delegate Implementation
    
    def textfield_did_end_editing(self, textfield):
        if textfield.name == "timezone_textfield":
            s = textfield.text
            try:
                zc = int(s)
                self.date.to_utc()
                self.date.set_zone_correction(zc)
                self.update_astrodate_panel()
            except ValueError:
                print "Exception converting %s to int!" % s
        elif textfield.name == "longitude_textfield":
            s = textfield.text
            try:
                lng = float(s)
                self.date.to_utc()
                self.date.set_longitude(lng)
                self.update_astrodate_panel()
            except ValueError:
                print "Exception converting %s to float!" % s
        elif textfield.name == "date_textfield":
            s = textfield.text
            ds = dts.DateTimeString(s)
            ds.parse_datetime()
            dat = ds.get_datetime_tuple()
            self.date.set_with_tuple(dat)
            self.update_astrodate_panel()
            
    # Switch Action Implementation
    
    def switch_changed(self, sender):
        if sender.name == "daylight_savings_switch":
            self.date.to_utc()
            self.date.set_daylight_savings(sender.value)
            self.update_astrodate_panel()


if __name__ == '__main__':
    

    main_view = ui.View(background_color=background_color)
    
    # make AstroDateView and add to main_view
    w = screen_width
    if w > 414:
        w = 414
    adv = AstroDateView(width=w)
    w, h = adv.make_astrodate_panel()
    adv.frame = (0, 0, w, h)
    main_view.add_subview(adv)
    adv.update_astrodate_panel()

    main_view.present('fullscreen')
    