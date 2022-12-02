import tkinter
import pandas as pd
from tkinter import ttk
import numpy
from tkinter import *
#Program that takes Mercedes Car 'data' and formats onto a GUI with
#tkinter. Options to manipulate the dataframe on the GUI with filter widgets
#and narrow down the list of cars you are searching for.
class CarFilter:
    def __init__(self):
        #reset StringVars of widgets
        def reset_vars():
            model_var.set('Model Type')
            price_range_var.set('Price Range')
            interior_var.set('Colors-Interior')
            exterior_var.set('Colors-Exterior')
            condition_var.set('Car Condition')
            location_entry.delete(0,END)
            location_entry.insert(0,'Location')
        #filters df by price range from GUI
        def price_sort(df_filtered, min_max):
            if (min_max != 'Any' and min_max != 'Price Range'):
                #makes min and max value from StringVar
                range = str(min_max).split('-')
                min = int(range[0].strip().replace('k','000'))
                max = int(range[1].strip().replace('k','000'))
                #narrows the df to only the rows with a price within the min/max range.
                df_filtered = df_filtered[df_filtered['price'].between(min, max, inclusive='both')]

            return df_filtered
        #filters df by model type
        def model_sort(df_filtered, type):
            if (type != 'Any' and type != 'Model Type'):
                df_filtered = df_filtered[df_filtered['model_name'].str.contains(type, case=False)]

            return df_filtered
        #filters df by interior color of car
        def i_col_sort(df_filtered, i_col):
            if (i_col != 'Colors-Interior' and i_col != 'Any'):
                df_filtered = df_filtered[df_filtered['interior_color'].str.contains(i_col,case=False)]

            return df_filtered
        #sorts df by exterior color of car    
        def e_col_sort(df_filtered, e_col):
            if (e_col != 'Colors-Exterior' and e_col != 'Any'):
                df_filtered = df_filtered[df_filtered['exterior_color'].str.contains(e_col,case=False)]
            
            return df_filtered
        #sorts df by location of car
        #supposed to be by city or country, but simply checks if 
        #string inputted into entry is within the location column.    
        def loc_sort(df_filtered, loc):
            if (loc != 'Location' and loc != ''):
                #add code for inputted text of non locations
                df_filtered = df_filtered[df_filtered['location_id'].str.contains(loc, case=False)]
        
            return df_filtered
        #sorts df by condition of car
        def con_sort(df_filtered, con):
            if (con != 'Car Condition' and con != 'Any'):
                df_filtered = df_filtered[df_filtered['condition'].str.contains(con, case=False)]
        
            return df_filtered
        #command for apply button widget. Takes in all filter StringVar values
        #and calls there respective functions to sort and narrow the df.
        #Then displays the new df on gui.
        def apply_filters(df, type, e_col, i_col, range, con, loc):
            #deletes existing tree/spreadsheet (df on gui)
            my_tree.delete(*my_tree.get_children())
            df = model_sort(df, type)
            df = e_col_sort(df, e_col)
            df = i_col_sort(df, i_col)
            df = price_sort(df, range)
            df = con_sort(df, con)
            df = loc_sort(df, loc)
            #creating new treeview of filtered df
            my_tree['column'] = list(df.columns)
            my_tree['show'] = 'headings'
            for column in my_tree['column']:
                my_tree.heading(column, text=column)
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                my_tree.insert('', 'end', values=row)
            #resets display on filter widgets
            reset_vars()



        #Gui window
        window = tkinter.Tk()
        window.title('Sprout')
        window.geometry('1280x1000')
        my_frame = tkinter.Frame(window)
        my_frame.pack(pady=20,fill = tkinter.BOTH, expand = True)
        #reads in csv file of car info
        df = pd.read_csv('./db.csv')
        global df_filtered
        df_filtered = df
        #expands max number of rows/columns shown when printing a df
        pd.set_option("display.max_rows", 2000)
        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.width', 1000)
        #veritcal and horizontal scroll bar for df
        my_scrollbar = ttk.Scrollbar(my_frame, orient = 'vertical')
        my_scrollbar.pack(side='right', fill='y')
        my_xscrollbar = ttk.Scrollbar(my_frame, orient='horizontal')
        my_xscrollbar.pack(side='bottom',fill='x')
        
        #creation of initial treewidget/ df with all data.
        global my_tree
        my_tree = tkinter.ttk.Treeview(my_frame, yscrollcommand=my_scrollbar.set,xscrollcommand=my_xscrollbar.set)
        my_scrollbar.config(command=my_tree.yview)
        my_xscrollbar.config(command=my_tree.xview)
        my_tree['column'] = list(df.columns)
        my_tree['show'] = 'headings'
        for column in my_tree['column']:
            my_tree.heading(column, text=column)


        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            my_tree.insert('', 'end', values=row)





        #Price widget
        price_range_var = tkinter.StringVar(window)
        price_range_var.set('Price Range')
        price_label = Label(window, text='Price Range')
        price_range = [
            '0 - 25k',
            '25k - 50k',
            '50k - 75k',
            '75k - 100k',
            '100k - 125k',
            '125k - 150k',
            '150k - 175k',
            '175k - 200k',
            'Any'
        ]
        price_range_tab = OptionMenu(window, price_range_var, *price_range)


        #Location Widget/Entry
        location_label = Label(window, text='Location:')
        location_entry = Entry(window, width=15)
        location_entry.insert(0,'Location')
        
        #Model widget
        models = [
            'SEDAN',
            'CABRIOLET',
            'COUPE',
            'WAGON',
            'SUV',
            'AMG',
            'MAYBACH',
            'ROADSTER',
            'Any'
        ]

        model_var = tkinter.StringVar(window)
        model_var.set('Model Type')
        model_label = Label(window, text='Model Type:')
        model_tab = OptionMenu(window, model_var, *models)

        #Style Widgets
        style_label = Label(window, text='Color Styles')
        interior_var = tkinter.StringVar(window)
        exterior_var = tkinter.StringVar(window)
        interior_var.set('Colors-Interior')
        exterior_var.set('Colors-Exterior')
        interior_colors = [
            'Red',
            'Black',
            'Beige',
            'Any'
        ]
        exterior_colors = [
            'Polar_White',
            'Night_Black',
            'Denim_Blue',
            'Red_Metallic',
            'Any'
        ]
        interior_style = OptionMenu(window, interior_var, *interior_colors)
        exterior_style = OptionMenu(window, exterior_var, *exterior_colors)

        #Condition widget
        condition = [
            'New',
            'Used',
            'Any'
        ]
        condition_var = tkinter.StringVar(window)
        condition_var.set('Car Condition')
        condition_label = Label(window, text='Car Condtion:')
        condition_tab = OptionMenu(window, condition_var, *condition)

        #Apply Filter widget. Calls the apply_filter() function with the df and the StringVar of all filters
        apply = Button(window, text='Apply Filters',
                        command= lambda: 
                        apply_filters(
                        df,
                        model_var.get(), exterior_var.get(),
                        interior_var.get(), price_range_var.get(), 
                        condition_var.get(), location_entry.get()
                        ))

        #Packing/Pushing of Widgets onto the window
        filler_label = Label(window,text='---------')
        filler2_label= Label(window,text='---------')
        filler3_label= Label(window,text='---------')
        filler4_label= Label(window,text='---------')
        filler5_label= Label(window,text='---------')
        filler6_label= Label(window,text='---------')
        model_tab.pack(side=LEFT, anchor=tkinter.S)
        filler3_label.pack(side=LEFT, anchor=tkinter.S)
        exterior_style.pack(side=LEFT,anchor=tkinter.S)
        filler2_label.pack(side=LEFT, anchor=tkinter.S)
        interior_style.pack(side=LEFT, anchor=tkinter.S)
        filler_label.pack(side=LEFT, anchor=tkinter.S)
        price_range_tab.pack(side=LEFT, anchor=tkinter.S)
        filler4_label.pack(side=LEFT, anchor=tkinter.S)
        condition_tab.pack(side=LEFT, anchor=tkinter.S)
        filler5_label.pack(side=LEFT, anchor=tkinter.S)
        location_entry.pack(side=LEFT, anchor=tkinter.S, pady=3)
        filler6_label.pack(side=LEFT, anchor=tkinter.S)
        apply.pack(side=LEFT,anchor=tkinter.S)
        my_tree.pack(fill=tkinter.BOTH, expand=True)

        window.mainloop()
CarFilter()
