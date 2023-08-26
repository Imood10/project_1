

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.popup import Popup
from kivy.uix.label import Label


# Your layouts.
Builder.load_string(
    '''
#:import os os
#:import Window kivy.core.window.Window
#:import IconLeftWidget kivymd.uix.list.IconLeftWidget
#:import images_path kivymd.images_path


<ItemBackdropFrontLayer@TwoLineAvatarListItem>



<MyBackdropFrontLayer@ItemBackdropFrontLayer>
    backdrop: None

    on_press: root.backdrop.open(-Window.height / 2)
    pos_hint: {"top": 1}
    _no_ripple_effect: True
    MDTextField:
        id: name_input  # Assign an ID to the name input widget

    MDTextField:
        id: email_input  # Assign an ID to the email input widget

    MDTextField:
        id: phone_input  # Assign an ID to the phone input widget

<MyBackdropBackLayer@Image>
    size_hint: .8, .8
    source: os.path.join(images_path, "logo", "kivymd-icon-512.png")
    pos_hint: {"center_x": .5, "center_y": .6}
'''
)

# Usage example of MDBackdrop.
Builder.load_string(
    '''
<ExampleBackdrop>

    MDBackdrop:
        id: backdrop
        left_action_items: [['menu', lambda x: self.open()]]
        title: "Example Backdrop"
        radius_left: "25dp"
        radius_right: "0dp"
        header_text: "Hello !"

        MDBackdropBackLayer:
            MyBackdropBackLayer:
                id: backlayer

        MDBackdropFrontLayer:
            MyBackdropFrontLayer:
                backdrop: backdrop


                MDTextField:
                    hint_text: "Enter Name"
                    helper_text_mode: "on_focus"
                    required: True
                    icon_right: "account"
                    icon_right_color: app.theme_cls.primary_color
                    pos_hint:{'center_x': 0.5, 'center_y': 0.9}
                    size_hint_x:None
                    width:300
                MDTextField:
                    hint_text: "Enter Email"
                    helper_text_mode: "on_focus"
                    required: True
                    icon_right: "email"
                    icon_right_color: app.theme_cls.primary_color
                    pos_hint:{'center_x': 0.5, 'center_y': 0.1}
                    size_hint_x:None
                    width:300

                MDTextField:
                    hint_text: "Enter Phone No."
                    helper_text_mode: "on_focus"
                    required: True
                    icon_right: "cellphone"
                    icon_right_color: app.theme_cls.primary_color
                    pos_hint:{'center_x': 0.5, 'center_y': -0.6}
                    size_hint_x:None
                    width:300

                MDLabel:
                    text: 'Gas Station 1'
                    pos_hint: {'center_x': 0.25, 'center_y':-1.5}
                    size_hint_x: None
                    width: dp(120)    

                MDCheckbox:
                    id: checkbox_1
                    group: 'options'
                    pos_hint: {'center_x': 0.25, 'center_y': -1.8}
                    size_hint: None, None
                    size: dp(30), dp(30)
                    active: True


                MDLabel:
                    text: 'Gas Station 2'
                    size_hint_x: None
                    pos_hint: {'center_x': 0.5, 'center_y': -1.5}
                    width: dp(120)    

                MDCheckbox:
                    id: checkbox_2
                    group: 'Gas Station 2'
                    specific_text_color: 1, 1, 1, 1
                    group: 'options'
                    pos_hint: {'center_x': 0.5, 'center_y': -1.8}
                    size_hint: None, None
                    size: dp(30), dp(30)
                    active: False


                MDLabel:
                    text: 'Gas Station 3'
                    size_hint_x: None
                    pos_hint: {'center_x': 0.78, 'center_y': -1.5}
                    width: dp(100)    

                MDCheckbox:
                    id: checkbox_3
                    group: 'options'
                    pos_hint: {'center_x': 0.75, 'center_y': -1.8}
                    size_hint: None, None
                    size: dp(30), dp(30)
                    active: False

                MDDropDownItem:
                    id: dropdown_item
                    text: 'Location'
                    on_release: app.menu.open()
                    pos_hint: {'center_x': .5, 'center_y': -2.6}


                MDRaisedButton:
                    text: "Submit"
                    pos_hint: {'center_x': 0.5, 'center_y': -3.5}
                    on_release: app.submit_form()   

'''
)


class MyBackdropBackLayer(BoxLayout):
    pass

class MyBackdropFrontLayer(BoxLayout):
    pass

class ExampleBackdrop(MDScreen):
    pass

class Example(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.fruits = [
            "Amina Hostel", "Alex Hostel", "Danfodio Hostel", "Dangote Hostel", "Icsa Hostel",
            "Ramat Hostel", "Ribadu Hostel", "Shehu Idris Hostel", "Suleiman Hostel"
        ]

        self.root_widget = ExampleBackdrop()

        dropdown_item = self.root_widget.ids.dropdown_item
        dropdown_item.bind(on_release=self.show_menu)

        self.menu = None

        return self.root_widget

    def show_menu(self, dropdown_item):
        self.menu = MDDropdownMenu(
            caller=dropdown_item,
            items=[
                {"text": fruit, "viewclass": "OneLineListItem", "on_release": lambda x=fruit: self.menu_item_selected(x)}
                for fruit in self.fruits
            ],
            width_mult=4,
        )
        self.menu.open()

    def menu_item_selected(self, selected_fruit):
        self.root_widget.ids.dropdown_item.text = selected_fruit
        self.menu.dismiss()

    def show_popup(self):
        content = Label(text="Request Sent!")
        self.popup = Popup(title="Submission Status", content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def submit_form(self):
        selected_fruit = self.root_widget.ids.dropdown_item.text
        name = self.root_widget.ids.my_front_layer.ids.name_input.text  # Adjust this line
        email = self.root_widget.ids.my_front_layer.ids.email_input.text  # Adjust this line
        phone = self.root_widget.ids.my_front_layer.ids.phone_input.text  # Adjust this line

        # Send the collected data to a specified email address
        self.send_email(selected_fruit, name, email, phone)

        self.show_popup()

    def send_email(self, selected_fruit, name, email, phone):
        from_email = email
        to_email = "recipient@example.com"
        subject = "Form Submission"
        message = f"Selected Fruit: {selected_fruit}\nName: {name}\nEmail: {email}\nPhone: {phone}"

        # Create a MIME message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, 'your_password_or_app_password')
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

if __name__ == "__main__":
    app = Example()
    app.run()
