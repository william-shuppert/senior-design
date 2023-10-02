"""Frameworks for running multiple Streamlit applications as a single app.
"""
from unicodedata import category
import streamlit as st

def findChange():
    for i in range(len(st.session_state.cat_new)):
        if (st.session_state.cat_new)[i] != (st.session_state.cat_last)[i]:
            return (st.session_state.cat_new)[i]
    return "" # no change / first run

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self, backend):
        self.categories = {}
        self.apps = []
        self.backend = backend


    def add_category(self, category, apps):
        """Adds a new application.
        Parameters
        ----------
        category:
            the category name.
        apps:
            a dictionary of apps under the category. Appears in the radio button in the sidebar.
        """
        self.categories[category] = []
        for key in apps:
            self.categories[category].append({
                                    "title": key,
                                    "function": apps[key]
                                })
    
    def run(self):
        # Radio buttons to select the category
        st.set_page_config(layout="wide")
        st.sidebar.title('Navigation')
        category = st.sidebar.radio(
            'Select Category:',
            self.categories.keys())

        # Radio buttons to select the page to run 
        app = st.sidebar.radio(
            'Select App',
            self.categories[category],
            format_func=lambda app: app['title'])

        st.sidebar.caption('For more information please contact Ming Chen: cming3425@gmail.com')
        # run the app function 
        app['function'](self.backend)

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run_radio(self):
        # Radio buttons to select the page to run 
        st.set_page_config(layout="wide")
        st.sidebar.title('Navigation')
        app = st.sidebar.radio(
            'Select App',
            self.apps,
            format_func=lambda app: app['title'])

        # run the app function 
        app['function'](self.backend)

    def run_dropdown(self):
        # Drodown to select the page to run  
        app = st.sidebar.selectbox(
            'App Navigation', 
            self.apps, 
            format_func=lambda app: app['title']
        )

        # run the app function 
        app['function']()