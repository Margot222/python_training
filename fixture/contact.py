from model.contact import Contact
import time
import re


class ContactHelper:

    def __init__(self, app):
        self.app = app

    def open_home_page(self):
        # return to groups page
        driver = self.app.driver
        if not driver.current_url.endswith("/addressbook/"):
            driver.find_element_by_link_text("home").click()

    def add_new_contact(self, contact):
        # add new contact
        driver = self.app.driver
        driver.find_element_by_link_text("add new").click()
        self.fill_contact_form(contact)
        driver.find_element_by_name("submit").click()
        self.contact_cache = None

    def fill_contact_form(self, contact):
        driver = self.app.driver
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("home", contact.homephone)
        self.change_field_value("mobile", contact.mobilephone)
        self.change_field_value("work", contact.workphone)
        self.change_field_value("phone2", contact.secondaryphone)

    def change_field_value(self, field_name, text):
        driver = self.app.driver
        if text is not None:
            driver.find_element_by_name(field_name).click()
            driver.find_element_by_name(field_name).clear()
            driver.find_element_by_name(field_name).send_keys(text)

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            driver = self.app.driver
            self.open_home_page()
            self.contact_cache = []
            for row in driver.find_elements_by_name("entry"):
                cells = row.find_elements_by_tag_name("td")
                firstname = cells[2].text
                lastname = cells[1].text
                id = cells[0].find_element_by_tag_name("input").get_attribute("value")
                all_phones = cells[5].text
                self.contact_cache.append(Contact(firstname=firstname, lastname=lastname, id=id, all_phones_from_home_page=all_phones))
        return list(self.contact_cache)

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        driver = self.app.driver
        # select first contact
        self.select_contact_by_index(index)
        # submit deletion
        driver.find_element_by_xpath("//div[2]/input").click()
        driver.switch_to_alert().accept()
        time.sleep(5)
        self.open_home_page()
        self.contact_cache = None

    def delete_contact_by_id(self, id):
        driver = self.app.driver
        # select first contact
        self.select_contact_by_id(id)
        # submit deletion
        driver.find_element_by_xpath("//div[2]/input").click()
        driver.switch_to_alert().accept()
        time.sleep(5)
        self.open_home_page()
        self.contact_cache = None

    def modify_first_contact(self, new_contact_data):
        self.modify_contact_by_index(new_contact_data, 0)

    def modify_contact_by_index(self, new_contact_data, index):
        driver = self.app.driver
        # open modification form
        self.open_contact_to_edit_by_index(index)
        # fill group form
        self.fill_contact_form(new_contact_data)
        # submit modification
        driver.find_element_by_name("update").click()
        driver.find_element_by_link_text("home page").click()
        self.contact_cache = None

    def select_first_contact(self):
        self.select_contact_by_index(0)

    def select_contact_by_index(self, index):
        driver = self.app.driver
        driver.find_elements_by_name("selected[]")[index].click()

    def select_contact_by_id(self, id):
        driver = self.app.driver
        driver.find_element_by_css_selector("input[id='%s']" % id).click()

    def count(self):
        driver = self.app.driver
        self.open_home_page()
        return len(driver.find_elements_by_name("selected[]"))

    def open_contact_to_edit_by_index(self, index):
        driver = self.app.driver
        self.open_home_page()
        row = driver.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_to_view_by_index(self, index):
        driver = self.app.driver
        self.open_home_page()
        row = driver.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def get_contact_info_from_edit_page(self, index):
        self.open_contact_to_edit_by_index(index)
        driver = self.app.driver
        firstname = driver.find_element_by_name("firstname").get_attribute("value")
        lastname = driver.find_element_by_name("lastname").get_attribute("value")
        id = driver.find_element_by_name("id").get_attribute("value")
        homephone = driver.find_element_by_name("home").get_attribute("value")
        workphone = driver.find_element_by_name("work").get_attribute("value")
        mobilephone = driver.find_element_by_name("mobile").get_attribute("value")
        secondaryphone = driver.find_element_by_name("phone2").get_attribute("value")
        return Contact(firstname=firstname, lastname=lastname, id=id, homephone=homephone, workphone=workphone, mobilephone=mobilephone, secondaryphone=secondaryphone)

    def get_contact_from_view_page(self, index):
        self.open_contact_to_view_by_index(index)
        driver = self.app.driver
        text = driver.find_element_by_id("content").text
        return Contact(all_phones_from_view_page=text)
