import astrocore.astrodate as ad
import astrocore.datetimestring as dts
import ui


main_view = None


class AstroDateView:

    def __init__(self):
        self.date = ad.AstroDate().alloc_now_utc()
        self.label_font = ('<system>', 12)
        self.content_font = ('<system>', 18)
        self.label_color = 'gray'
        self.width = 300

    def make_astrodate_panel(self):
        v = ui.View(background_color='clear', name="datetime_view")
    
        x, y, w, h = 0, 0, self.width, 21
        date_label = ui.Label(frame=(x, y, w, h), text="Current Date/Time")
        date_label.font = self.label_font
        date_label.text_color = self.label_color
        v.add_subview(date_label)
    
        x, y, w, h = 0, y + h, self.width, 30
        date_textfield = ui.TextField(frame=(x, y, w, h))
        date_textfield.delegate = self
        date_textfield.name = "date_textfield"
        date_textfield.text = self.date.get_pretty_string()
        v.add_subview(date_textfield)
    
        x, y, w, h = 0, y + h, 100, 21
        timezone_label = ui.Label(frame=(x, y, w, h), text="Time Zone")
        timezone_label.font = self.label_font
        timezone_label.text_color = self.label_color
        v.add_subview(timezone_label)
    
        x, y, w, h = x + w, y, 50, h
        daysave_label = ui.Label(frame=(x, y, w, h), text="Daylight")
        daysave_label.font = self.label_font
        daysave_label.text_color = self.label_color
        v.add_subview(daysave_label)
    
        x, y, w, h = x + w, y, 150, h
        longitude_label = ui.Label(frame=(x, y, w, h), text="Longitude")
        longitude_label.font = self.label_font
        longitude_label.text_color = self.label_color
        v.add_subview(longitude_label)
    
        x, y, w, h = 0, y + h, 99, 30
        timezone_textfield = ui.TextField(frame=(x, y, w, h))
        timezone_textfield.delegate = self
        timezone_textfield.name = "timezone_textfield"
        timezone_textfield.text = "%d" % self.date.get_zone_correction()
        v.add_subview(timezone_textfield)
    
        x, y, w, h = x + w + 1, y, 50, h
        daysave_switch = ui.Switch(frame=(x, y, w, h))
        daysave_switch.action = self.switch_changed
        daysave_switch.name = "daylight_savings_switch"
        daysave_switch.value = self.date.get_daylight_savings()
        v.add_subview(daysave_switch)
    
        x, y, w, h = x + w + 1, y, 149, h
        longitude_textfield = ui.TextField(frame=(x, y, w, h))
        longitude_textfield.delegate = self
        longitude_textfield.name = "longitude_textfield"
        longitude_textfield.text = "%.5f" % self.date.get_longitude()
        v.add_subview(longitude_textfield)
    
        x, y, w, h = 5, y + h + 5, self.width, 21
        label = ui.Label(frame=(x, y, w, h))
        label.name = "lct_label"
        label.font = self.content_font
        label.text_color = self.label_color
        v.add_subview(label)
    
        x, y, w, h = 5, y + h + 5, self.width, 21
        label = ui.Label(frame=(x, y, w, h))
        label.name = "utc_label"
        label.font = self.content_font
        label.text_color = self.label_color
        v.add_subview(label)

        x, y, w, h = 15, y + h + 5, self.width, 21
        label = ui.Label(frame=(x, y, w, h))
        label.name = "utc_jd_label"
        label.font = self.content_font
        label.text_color = self.label_color
        v.add_subview(label)

        x, y, w, h = 5, y + h + 5, self.width, 21
        label = ui.Label(frame=(x, y, w, h))
        label.name = "tdt_label"
        label.font = self.content_font
        label.text_color = self.label_color
        v.add_subview(label)

        x, y, w, h = 15, y + h + 5, self.width, 21
        label = ui.Label(frame=(x, y, w, h))
        label.name = "tdt_jd_label"
        label.font = self.content_font
        label.text_color = self.label_color
        v.add_subview(label)
            
        x, y, w, h = 5, y + h + 5, self.width, 21
        label = ui.Label(frame=(x, y, w, h))
        label.name = "gst_label"
        label.font = self.content_font
        label.text_color = self.label_color
        v.add_subview(label)

        x, y, w, h = 5, y + h + 5, self.width, 21
        label = ui.Label(frame=(x, y, w, h))
        label.name = "lst_label"
        label.font = self.content_font
        label.text_color = self.label_color
        v.add_subview(label)
                   
        v.frame = (0, 0, self.width, y + h)
        return v
    
    def set_text_in_label(self, name, text):
        dtv = main_view["datetime_view"]
        if dtv is not None:
            label = dtv[name]
            if label is not None:
                label.text = text

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
    

    main_view = ui.View(background_color='black')
    
    adv = AstroDateView()
    v = adv.make_astrodate_panel()
    main_view.add_subview(v)
    
    adv.update_astrodate_panel()

    main_view.present('fullscreen')
