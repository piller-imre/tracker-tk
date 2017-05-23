import tkinter
from tkinter import ttk
from tracker import Tracker
from models import create_database_session


def create_new_category():
    """Create new category."""
    print('Create new category ...')


def rename_category():
    """Rename the category."""
    print('Rename the category ...')


def change_category_type():
    """Change the type of the category."""
    print('Change the type of the category ...')


def remove_category():
    """Remove the selected category."""
    print('Remove the selected category ...')


def save_measurement():
    """Save the measurement."""
    print('Save the measurement ...')


def edit_measurement():
    """Edit the selected measurement."""
    print('Edit the selected measurement ...')


def remove_measurement():
    """Remove the selected measurement."""
    print('Remove the selected measurement ...')


if __name__ == '__main__':

    database_session = create_database_session('sqlite:////tmp/tracker.db')
    Tracker(database_session)

    root = tkinter.Tk()
    root.title('Tracker')

    new_category_button = tkinter.Button(root, text='New', command=create_new_category)
    rename_category_button = tkinter.Button(root, text='Rename', command=rename_category)
    change_category_button = tkinter.Button(root, text='Change', command=change_category_type)
    remove_category_button = tkinter.Button(root, text='Remove', command=remove_category)
    category_combobox = ttk.Combobox(root)
    measurement_entry = tkinter.Entry(root)
    save_measurement_button = tkinter.Button(root, text='Save', command=save_measurement)
    measurement_list = ttk.Treeview(root)
    edit_measurement_button = tkinter.Button(root, text='Edit', command=edit_measurement)
    remove_measurement_button = tkinter.Button(root, text='Remove', command=remove_measurement)

    full = (tkinter.N, tkinter.S, tkinter.E, tkinter.W)
    new_category_button.grid(row=0, column=0, sticky=full)
    rename_category_button.grid(row=0, column=1, sticky=full)
    change_category_button.grid(row=0, column=2, sticky=full)
    remove_category_button.grid(row=0, column=3, sticky=full)
    category_combobox.grid(row=1, column=0, columnspan=4, sticky=full)
    measurement_entry.grid(row=2, column=0, columnspan=3, sticky=full)
    save_measurement_button.grid(row=2, column=3, sticky=full)
    measurement_list.grid(row=3, column=0, columnspan=4, sticky=full)
    edit_measurement_button.grid(row=4, column=0, columnspan=2, sticky=full)
    remove_measurement_button.grid(row=4, column=2, columnspan=2, sticky=full)

    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=0)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=0)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)

    root.mainloop()
