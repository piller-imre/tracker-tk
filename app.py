import tkinter
from tkinter import messagebox
from tkinter import ttk
from tracker import Tracker
from models import create_database_session


database_session = create_database_session('sqlite:////tmp/tracker.db')
tracker = Tracker(database_session)


def show_categories():
    """Show the categories in the category combobox."""
    category_combobox['values'] = tracker.list_categories()


def show_measurements():
    """Show the measurements in the measurement list."""
    category_name = category_combobox.get()
    if category_name != '':
        measurement_list.delete(*measurement_list.get_children())
        for measurement in tracker.list_measurements(category_name):
            measurement_list.insert('', 0, iid=measurement.id, text=str(measurement.id), values=[str(measurement.value), str(measurement.timestamp)])


def create_new_category():
    """Create new category."""
    print('Create new category ...')
    category_name = measurement_entry.get()
    if category_name != '':
        try:
            tracker.create_category(category_name)
            show_categories()
        except ValueError as error:
            messagebox.showerror('Error', error)
    else:
        messagebox.showerror('Missing category name!', 'You have forgot to set proper category name!')


def rename_category():
    """Rename the category."""
    new_name = measurement_entry.get()
    old_name = category_combobox.get()
    if old_name != '':
        if new_name != '':
            question = 'Do you want to rename the category from "{}" to "{}"?'.format(old_name, new_name)
            if messagebox.askokcancel('Category renaming', question):
                tracker.rename_category(old_name, new_name)
                show_categories()
        else:
            messagebox.showerror('Missing category name!', 'You have forgot to set the new category name!')
    else:
        messagebox.showerror('Missing category name!', 'You have to select the category for renaming!')


def change_category_type():
    """Change the type of the category."""
    print('Change the type of the category ...')
    messagebox.showinfo('Info', 'Not implemented yet!')


def remove_category():
    """Remove the selected category."""
    category_name = category_combobox.get()
    if category_name != '':
        if messagebox.askokcancel('Remove category', 'Do you want to remove the category "{}"?'.format(category_name)):
            tracker.remove_category(category_name)
            show_categories()
    else:
        messagebox.showerror('Missing category name!', 'You have to select the category for removing!')


def select_category(event):
    """Select category in the combobox."""
    show_measurements()


def save_measurement():
    """Save the measurement."""
    category_name = category_combobox.get()
    if category_name != '':
        value = measurement_entry.get()
        if value != '':
            tracker.save_measurement(category_name, value)
            show_measurements()
        else:
            messagebox.showerror('Missing measurement value!', 'The measurement value is missing!')
    else:
        messagebox.showerror('Missing category name!', 'You have to select the category for saving measurement!')


def edit_measurement():
    """Edit the selected measurement."""
    selected = measurement_list.selection()
    if len(selected) == 1:
        measurement_id = int(selected[0])
        value = measurement_entry.get()
        if value != '':
            tracker.correct_measurement(measurement_id, value)
            show_measurements()
        else:
            messagebox.showerror('Missing measurement value!', 'The measurement value is missing!')
    else:
        messagebox.showerror('Selection error', 'There are {} selected items instead of 1!'.format(len(selected)))


def remove_measurement():
    """Remove the selected measurement."""
    selected = measurement_list.selection()
    if len(selected) == 1:
        measurement_id = int(selected[0])
        if messagebox.askokcancel('Remove measurement', 'Do you want to remove the measurement?'):
            tracker.remove_measurement(measurement_id)
            show_measurements()
    else:
        messagebox.showerror('Selection error', 'There are {} selected items instead of 1!'.format(len(selected)))


root = tkinter.Tk()
root.title('Tracker')

new_category_button = tkinter.Button(root, text='New', command=create_new_category)
rename_category_button = tkinter.Button(root, text='Rename', command=rename_category)
change_category_button = tkinter.Button(root, text='Change', command=change_category_type)
remove_category_button = tkinter.Button(root, text='Remove', command=remove_category)
category_combobox = ttk.Combobox(root)
category_combobox.bind('<<ComboboxSelected>>', select_category)
measurement_entry = tkinter.Entry(root, background='#FFCCAA')
save_measurement_button = tkinter.Button(root, text='Save', command=save_measurement)
measurement_list = ttk.Treeview(root, columns=('measurement', 'timestamp'))
measurement_list.heading('measurement', text='measurement')
measurement_list.heading('timestamp', text='timestamp')
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

show_categories()

root.mainloop()
