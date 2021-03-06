from model.contact import Contact
from random import randrange


def test_modify_contact_name(app):
    if app.contact.count() == 0:
        app.contact.add_new_contact(Contact("ftest", "mtest", "ltest", "ntest"))
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact = Contact(firstname="MODIFIED")
    contact.id = old_contacts[index].id
    contact.lastname = old_contacts[index].lastname
    app.contact.modify_contact_by_index(contact, index)
    assert len(old_contacts) == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts[index] = contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)

#def test_modify_contact_lastname(app):
#    if app.contact.count() == 0:
 #       app.contact.create(Contact("ftest", "mtest", "ltest", "ntest")))
#    app.contact.modify_first_contact(Contact(name="New last name"))
