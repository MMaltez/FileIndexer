#!/usr/bin/env python
"""
@author Miguel Maltez Jose
@date 20160807
"""
import sys
import Tkinter as tk
import ttk
from FHLUtil import *

class DupSelector(tk.Frame):
	def __init__(self, master=None, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self.pack(fill=tk.BOTH, expand=True)
		self.createWidgets()

	def createWidgets(self):
		"""Populate Application frame with wigets."""
		# TABLE
		self.tableFrame = tk.Frame(self)
		self.tableFrame.pack(fill=tk.BOTH, expand=True)
		self.tv = ttk.Treeview(self.tableFrame
			, columns=("size","modified", "path"))
		self.tv.pack(fill=tk.BOTH, expand=True)
		# set column headings
		self.tv.heading("#0",       text="SHA1")
		self.tv.heading("size",     text="size")
		self.tv.heading("modified", text="modified")
		self.tv.heading("path",     text="path")
		# format columns
		self.tv.column("#0", anchor=tk.W, stretch=0)
		self.tv.column("size", anchor=tk.E, width=80, stretch=0)
		self.tv.column("modified", anchor=tk.E, width=160, stretch=0)
		# scroll bars
		vsb = ttk.Scrollbar(self.tv, orient="vertical", command=self.tv.yview)
		hsb = ttk.Scrollbar(self.tv, orient="horizontal", command=self.tv.xview)
		self.tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
		vsb.pack(side=tk.RIGHT, fill=tk.Y)
		hsb.pack(side=tk.BOTTOM, fill=tk.X)
		
		# BUTTONS
		self.btnFrame = tk.Frame(self)
		self.btnFrame.grid_propagate(0)
		self.btnFrame.pack()
		
		self.btnQuit = tk.Button(self.btnFrame
			, text="QUIT", command=self.quit)
		self.btnQuit.pack({"side": "left"})

		self.btnPrintf = tk.Button(self.btnFrame
			, text="print selected", command=self.printSelected)
		self.btnPrintf.pack({"side": "left"})
	
	def insertSHA1FileList(self, sha1, size, filelist):
		"""Insert a list of files with same SHA1 into the treeview."""
		branch = self.tv.insert("", "end", open=True
 			, text=sha1, values=(size,)
			, tags=("sha1",))
		self.tv.tag_configure("sha1", font=("Courier", 0, ""))
		for item in filelist:
			self.tv.insert(branch, "end"
				, values=(item[-3],item[-2],item[-1])
				, tags=("data",))
		self.tv.tag_configure("data", font=("",0,"normal"))
	
	def printSelected(self):
		"""Write selected filenames to stdout."""
		#print self.__class__.__name__ + "." + self.printf.__name__ + " called"
		sel = self.tv.selection()
		for item in sel:
			values = self.tv.item(item)["values"]
			if len(values) >= 3:
				print values[2]
	
def main():
	top=tk.Tk()
	top.geometry("800x600")
	top.title("Duplicate Selector")
	app = DupSelector(top)

	# load file hash list from file
	fhlfile = open("sample.fhl" if len(sys.argv)<2 else sys.argv[1])
	fhl = loadFHL(fhlfile)
	# group files by SHA1
	freq, size, groups = groupBySHA1(fhl)
	# filter in files with duplicated hashes
	ws = [ (sha1, size[sha1]) for sha1 in freq if freq[sha1] > 1 ]
	# sort groups by size
	ws.sort(key=lambda x: x[1], reverse=True)
	
	for key,s in ws:
		groups[key].sort(key=lambda x: x[4])
		app.insertSHA1FileList(key, s, groups[key])
	
	app.mainloop()

if __name__ == "__main__":
	main()
