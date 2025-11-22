import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from database import Database
import re

class ModernExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e2e")
        
        # Color scheme
        self.colors = {
            'bg': '#1e1e2e',
            'card': '#2d2d44',
            'accent': '#6c5ce7',
            'accent_hover': '#5f4fd4',
            'text': '#ffffff',
            'text_secondary': '#a0a0a0',
            'success': '#00b894',
            'danger': '#d63031',
            'warning': '#fdcb6e',
            'input': '#3d3d5c'
        }
        
        self.db = Database()
        self.current_user_id = None
        self.current_user = None
        
        # Configure style
        self.setup_styles()
        
        # Show login screen
        self.show_login()
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=10)
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_hover']),
                            ('pressed', self.colors['accent_hover'])])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=5)
        style.map('Danger.TButton',
                 background=[('active', '#c02a2a')])
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Display login/registration screen"""
        self.clear_window()
        
        # Main container
        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True)
        
        # Center frame
        center_frame = tk.Frame(container, bg=self.colors['card'], width=400, height=500)
        center_frame.pack(expand=True)
        center_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(center_frame, text="💰 Expense Tracker", 
                              font=('Segoe UI', 28, 'bold'),
                              bg=self.colors['card'], fg=self.colors['text'])
        title_label.pack(pady=(40, 10))
        
        subtitle = tk.Label(center_frame, text="Track your expenses effortlessly",
                           font=('Segoe UI', 12),
                           bg=self.colors['card'], fg=self.colors['text_secondary'])
        subtitle.pack(pady=(0, 40))
        
        # Login form
        self.login_frame = tk.Frame(center_frame, bg=self.colors['card'])
        self.login_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Username
        tk.Label(self.login_frame, text="Username", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.username_entry = tk.Entry(self.login_frame, font=('Segoe UI', 11),
                                      bg=self.colors['input'], fg=self.colors['text'],
                                      insertbackground=self.colors['text'],
                                      relief=tk.FLAT, bd=10)
        self.username_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(self.login_frame, text="Password", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.password_entry = tk.Entry(self.login_frame, font=('Segoe UI', 11),
                                      bg=self.colors['input'], fg=self.colors['text'],
                                      insertbackground=self.colors['text'],
                                      relief=tk.FLAT, bd=10, show='•')
        self.password_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Login button
        login_btn = ttk.Button(self.login_frame, text="Login", style='Accent.TButton',
                              command=self.handle_login)
        login_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Register button
        register_btn = tk.Button(self.login_frame, text="Create Account",
                                font=('Segoe UI', 10),
                                bg=self.colors['card'], fg=self.colors['accent'],
                                activebackground=self.colors['card'],
                                activeforeground=self.colors['accent_hover'],
                                relief=tk.FLAT, cursor='hand2',
                                command=self.handle_register)
        register_btn.pack(fill=tk.X)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        self.username_entry.focus()
    
    def handle_login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        user_id = self.db.authenticate_user(username, password)
        if user_id:
            self.current_user_id = user_id
            self.current_user = username
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def handle_register(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        
        if self.db.register_user(username, password):
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Username already exists")
    
    def show_dashboard(self):
        """Display main dashboard"""
        self.clear_window()
        
        # Top bar
        top_bar = tk.Frame(self.root, bg=self.colors['card'], height=60)
        top_bar.pack(fill=tk.X, padx=0, pady=0)
        top_bar.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(top_bar, text=f"Welcome, {self.current_user}!",
                                font=('Segoe UI', 14, 'bold'),
                                bg=self.colors['card'], fg=self.colors['text'])
        welcome_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Logout button
        logout_btn = tk.Button(top_bar, text="Logout", font=('Segoe UI', 10),
                              bg=self.colors['danger'], fg=self.colors['text'],
                              activebackground='#c02a2a', relief=tk.FLAT,
                              cursor='hand2', padx=15, pady=5,
                              command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main content area
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Add expense
        left_panel = tk.Frame(main_container, bg=self.colors['card'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Right panel - Expenses list and summary
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add expense form
        self.create_add_expense_form(left_panel)
        
        # Summary cards
        self.create_summary_cards(right_panel)
        
        # Expenses list
        self.create_expenses_list(right_panel)
        
        # Load initial data
        self.refresh_data()
    
    def create_add_expense_form(self, parent):
        """Create the add expense form"""
        form_title = tk.Label(parent, text="Add Expense", font=('Segoe UI', 18, 'bold'),
                             bg=self.colors['card'], fg=self.colors['text'])
        form_title.pack(pady=(20, 20))
        
        form_frame = tk.Frame(parent, bg=self.colors['card'])
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Amount
        tk.Label(form_frame, text="Amount", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.amount_entry = tk.Entry(form_frame, font=('Segoe UI', 11),
                                    bg=self.colors['input'], fg=self.colors['text'],
                                    insertbackground=self.colors['text'],
                                    relief=tk.FLAT, bd=10)
        self.amount_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Category
        tk.Label(form_frame, text="Category", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.category_var = tk.StringVar()
        categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 
                     'Healthcare', 'Education', 'Other']
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var,
                                     values=categories, font=('Segoe UI', 11),
                                     state='readonly', width=27)
        category_combo.pack(fill=tk.X, pady=(0, 15), ipady=8)
        category_combo.set(categories[0])
        
        # Description
        tk.Label(form_frame, text="Description", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.description_entry = tk.Entry(form_frame, font=('Segoe UI', 11),
                                         bg=self.colors['input'], fg=self.colors['text'],
                                         insertbackground=self.colors['text'],
                                         relief=tk.FLAT, bd=10)
        self.description_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Date
        tk.Label(form_frame, text="Date", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.date_entry = tk.Entry(form_frame, font=('Segoe UI', 11),
                                   bg=self.colors['input'], fg=self.colors['text'],
                                   insertbackground=self.colors['text'],
                                   relief=tk.FLAT, bd=10)
        self.date_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        self.date_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        # Add button
        add_btn = ttk.Button(form_frame, text="Add Expense", style='Accent.TButton',
                            command=self.add_expense)
        add_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Filter section
        filter_label = tk.Label(parent, text="Filters", font=('Segoe UI', 14, 'bold'),
                               bg=self.colors['card'], fg=self.colors['text'])
        filter_label.pack(pady=(20, 10))
        
        filter_frame = tk.Frame(parent, bg=self.colors['card'])
        filter_frame.pack(padx=20, pady=10, fill=tk.BOTH)
        
        # Category filter
        tk.Label(filter_frame, text="Category", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.filter_category_var = tk.StringVar()
        filter_cat_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var,
                                       values=['All'] + categories, font=('Segoe UI', 11),
                                       state='readonly', width=27)
        filter_cat_combo.pack(fill=tk.X, pady=(0, 10), ipady=8)
        filter_cat_combo.set('All')
        filter_cat_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_data())
        
        # Date range
        tk.Label(filter_frame, text="Start Date (optional)", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.start_date_entry = tk.Entry(filter_frame, font=('Segoe UI', 11),
                                         bg=self.colors['input'], fg=self.colors['text'],
                                         insertbackground=self.colors['text'],
                                         relief=tk.FLAT, bd=10)
        self.start_date_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        tk.Label(filter_frame, text="End Date (optional)", font=('Segoe UI', 10),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        self.end_date_entry = tk.Entry(filter_frame, font=('Segoe UI', 11),
                                       bg=self.colors['input'], fg=self.colors['text'],
                                       insertbackground=self.colors['text'],
                                       relief=tk.FLAT, bd=10)
        self.end_date_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        # Apply filter button
        filter_btn = tk.Button(filter_frame, text="Apply Filters", font=('Segoe UI', 10),
                              bg=self.colors['accent'], fg=self.colors['text'],
                              activebackground=self.colors['accent_hover'],
                              relief=tk.FLAT, cursor='hand2', padx=10, pady=8,
                              command=self.refresh_data)
        filter_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Clear filters button
        clear_btn = tk.Button(filter_frame, text="Clear Filters", font=('Segoe UI', 10),
                             bg=self.colors['input'], fg=self.colors['text'],
                             activebackground='#4d4d6c', relief=tk.FLAT,
                             cursor='hand2', padx=10, pady=8,
                             command=self.clear_filters)
        clear_btn.pack(fill=tk.X)
    
    def create_summary_cards(self, parent):
        """Create summary statistics cards"""
        summary_frame = tk.Frame(parent, bg=self.colors['bg'])
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Total expenses card
        self.total_card = tk.Frame(summary_frame, bg=self.colors['card'], width=200, height=120)
        self.total_card.pack(side=tk.LEFT, padx=(0, 15))
        self.total_card.pack_propagate(False)
        
        tk.Label(self.total_card, text="Total Expenses", font=('Segoe UI', 11),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(pady=(15, 5))
        self.total_label = tk.Label(self.total_card, text="$0.00", font=('Segoe UI', 24, 'bold'),
                                    bg=self.colors['card'], fg=self.colors['danger'])
        self.total_label.pack()
        
        # Count card
        self.count_card = tk.Frame(summary_frame, bg=self.colors['card'], width=200, height=120)
        self.count_card.pack(side=tk.LEFT, padx=(0, 15))
        self.count_card.pack_propagate(False)
        
        tk.Label(self.count_card, text="Total Transactions", font=('Segoe UI', 11),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(pady=(15, 5))
        self.count_label = tk.Label(self.count_card, text="0", font=('Segoe UI', 24, 'bold'),
                                    bg=self.colors['card'], fg=self.colors['accent'])
        self.count_label.pack()
        
        # Average card
        self.avg_card = tk.Frame(summary_frame, bg=self.colors['card'], width=200, height=120)
        self.avg_card.pack(side=tk.LEFT)
        self.avg_card.pack_propagate(False)
        
        tk.Label(self.avg_card, text="Average Expense", font=('Segoe UI', 11),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(pady=(15, 5))
        self.avg_label = tk.Label(self.avg_card, text="$0.00", font=('Segoe UI', 24, 'bold'),
                                  bg=self.colors['card'], fg=self.colors['success'])
        self.avg_label.pack()
    
    def create_expenses_list(self, parent):
        """Create the expenses list/table"""
        list_frame = tk.Frame(parent, bg=self.colors['bg'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(list_frame, text="Recent Expenses", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(list_frame, bg=self.colors['card'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ('Date', 'Category', 'Description', 'Amount')
        self.expenses_tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                         height=15, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.expenses_tree.yview)
        
        # Configure columns
        self.expenses_tree.heading('Date', text='Date')
        self.expenses_tree.heading('Category', text='Category')
        self.expenses_tree.heading('Description', text='Description')
        self.expenses_tree.heading('Amount', text='Amount')
        
        self.expenses_tree.column('Date', width=120, anchor='center')
        self.expenses_tree.column('Category', width=120, anchor='center')
        self.expenses_tree.column('Description', width=300, anchor='w')
        self.expenses_tree.column('Amount', width=120, anchor='e')
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", background=self.colors['card'], foreground=self.colors['text'],
                       fieldbackground=self.colors['card'], rowheight=30, font=('Segoe UI', 10))
        style.configure("Treeview.Heading", background=self.colors['input'],
                       foreground=self.colors['text'], font=('Segoe UI', 10, 'bold'))
        style.map("Treeview", background=[('selected', self.colors['accent'])])
        
        self.expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind double-click to delete
        self.expenses_tree.bind('<Double-1>', self.delete_selected_expense)
        
        # Delete button
        delete_btn = tk.Button(list_frame, text="Delete Selected", font=('Segoe UI', 10),
                              bg=self.colors['danger'], fg=self.colors['text'],
                              activebackground='#c02a2a', relief=tk.FLAT,
                              cursor='hand2', padx=15, pady=8,
                              command=self.delete_selected_expense)
        delete_btn.pack(pady=(10, 0))
    
    def add_expense(self):
        """Add a new expense"""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return
        
        category = self.category_var.get()
        description = self.description_entry.get().strip() or "No description"
        expense_date = self.date_entry.get().strip()
        
        # Validate date format
        try:
            datetime.strptime(expense_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Please enter date in YYYY-MM-DD format")
            return
        
        if self.db.add_expense(self.current_user_id, amount, category, description, expense_date):
            messagebox.showinfo("Success", "Expense added successfully!")
            # Clear form
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date.today().strftime('%Y-%m-%d'))
            # Refresh data
            self.refresh_data()
        else:
            messagebox.showerror("Error", "Failed to add expense")
    
    def refresh_data(self):
        """Refresh expenses list and summary"""
        # Get filters
        category_filter = self.filter_category_var.get()
        start_date = self.start_date_entry.get().strip() or None
        end_date = self.end_date_entry.get().strip() or None
        
        if category_filter == 'All':
            category_filter = None
        
        # Get expenses
        expenses = self.db.get_expenses(self.current_user_id, start_date, end_date, category_filter)
        
        # Clear treeview
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        # Populate treeview
        for expense in expenses:
            self.expenses_tree.insert('', 'end', iid=expense['id'],
                                     values=(expense['date'], expense['category'],
                                            expense['description'], f"${expense['amount']:.2f}"))
        
        # Update summary
        summary = self.db.get_expense_summary(self.current_user_id, start_date, end_date)
        self.total_label.config(text=f"${summary['total']:.2f}")
        self.count_label.config(text=str(summary['count']))
        
        if summary['count'] > 0:
            avg = summary['total'] / summary['count']
            self.avg_label.config(text=f"${avg:.2f}")
        else:
            self.avg_label.config(text="$0.00")
    
    def clear_filters(self):
        """Clear all filters"""
        self.filter_category_var.set('All')
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.refresh_data()
    
    def delete_selected_expense(self, event=None):
        """Delete selected expense"""
        selected = self.expenses_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
        
        expense_id = int(selected[0])
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            if self.db.delete_expense(expense_id, self.current_user_id):
                messagebox.showinfo("Success", "Expense deleted successfully")
                self.refresh_data()
            else:
                messagebox.showerror("Error", "Failed to delete expense")
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user_id = None
            self.current_user = None
            self.show_login()

def main():
    root = tk.Tk()
    app = ModernExpenseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()





