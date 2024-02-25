import tkinter as tk
from tkinter import simpledialog

class BlogPost:
    def __init__(self, post_number, title, text, tags, publication_date, visitors):
        self.post_number = post_number
        self.title = title
        self.text = text
        self.tags = tags
        self.publication_date = publication_date
        self.visitors = visitors

class PriorityQueue:
    def __init__(self):
        self.posts = []
    
    def insert(self, post):
        self.posts.append(post)
        self._heapify_up(len(self.posts) - 1)
    
    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.posts[index].visitors <= self.posts[parent_index].visitors:
                break
            self._swap(index, parent_index)
            index = parent_index
    
    def heap_sort(self):
        sorted_posts = []
        while self.posts:
            self._swap(0, len(self.posts) - 1)
            sorted_posts.append(self.posts.pop())
            self._heapify_down(0)
        return sorted_posts
    
    def _heapify_down(self, index):
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            largest = index
            if (left_child_index < len(self.posts) and self.posts[left_child_index].visitors > self.posts[largest].visitors):
                largest = left_child_index
            if (right_child_index < len(self.posts) and self.posts[right_child_index].visitors > self.posts[largest].visitors):
                largest = right_child_index
            if largest == index:
                break
            self._swap(index, largest)
            index = largest
    
    def _swap(self, i, j):
        self.posts[i], self.posts[j] = self.posts[j], self.posts[i]

class BlogGUI:
    def __init__(self, master):
        self.master = master
        master.title("Blog Post Manager")

        self.add_post_button = tk.Button(master, text="Add Blog Post", command=self.add_post)
        self.add_post_button.pack()

        self.sort_button = tk.Button(master, text="Sort Posts", command=self.sort_posts)
        self.sort_button.pack()

        self.display_button = tk.Button(master, text="Display Posts", command=self.display_posts)
        self.display_button.pack()

        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack()

        self.pq = PriorityQueue()


class Lab1:
    def __init__(self, parent):
        self.parent = parent
        self.pq = PriorityQueue()

    def create_interface(self):
        self.add_post_button = tk.Button(self.parent, text="Add Blog Post", command=self.add_post)
        self.add_post_button.pack()

        self.sort_button = tk.Button(self.parent, text="Sort Posts", command=self.sort_posts)
        self.sort_button.pack()

        self.display_button = tk.Button(self.parent, text="Display Posts", command=self.display_posts)
        self.display_button.pack()

        self.text_area = tk.Text(self.parent, height=10, width=50)
        self.text_area.pack()

    def add_post(self):
        post_number = simpledialog.askinteger("Input", "Enter post number", parent=self.parent)
        title = simpledialog.askstring("Input", "Enter title", parent=self.parent)
        text = simpledialog.askstring("Input", "Enter text", parent=self.parent)
        tags = simpledialog.askstring("Input", "Enter tags (comma-separated)", parent=self.parent).split(',')
        publication_date = simpledialog.askstring("Input", "Enter publication date (YYYY-MM-DD)", parent=self.parent)
        visitors = simpledialog.askinteger("Input", "Enter number of visitors", parent=self.parent)
        post = BlogPost(post_number, title, text, tags, publication_date, visitors)
        self.pq.insert(post)

    def sort_posts(self):
        sorted_posts = self.pq.heap_sort()
        self.text_area.delete(1.0, tk.END)
        for post in sorted_posts:
            self.text_area.insert(tk.END, f"Title: {post.title}, Tags: {post.tags}, Visitors: {post.visitors}\n")

    def display_posts(self):
        self.text_area.delete(1.0, tk.END)
        for post in self.pq.posts:
            self.text_area.insert(tk.END, f"Title: {post.title}, Tags: {post.tags}, Visitors: {post.visitors}\n")


# if __name__ == "__main__":
#     root = tk.Tk()
#     gui = BlogGUI(root)
#     root.mainloop()
