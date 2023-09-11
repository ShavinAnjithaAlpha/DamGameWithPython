from tkinter import *
from tkinter import colorchooser
from PIL import ImageTk, Image
import random


class DamGame(Tk):
    def __init__(self):
        super(DamGame, self).__init__()
        self.title("Dam Game version-2021.0.0")
        self.geometry("1000x700+0+0")
        self.config(bg="#1e1f21")

        # create the Menu
        self.main_menu = Menu(self)
        self.config(menu = self.main_menu)

        # create file menu
        self.file_menu = Menu(self)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        # create the edit menu
        self.edit_menu = Menu(self)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)

        self.file_menu.add_command(label="New Game", command=self.New_Game)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda :self.destroy())
        # command for edit menu
        self.edit_menu.add_command(label="color for black squares", command=lambda e="black":self.change_color(e))
        self.edit_menu.add_command(label="color for white squares", command=lambda e="white": self.change_color(e))

        # canvas width and height
        self.w = 500
        self.h = 500
        # create canvas for create Dam board
        self.canvas_1 = Canvas(self, width=self.w, height=self.h, bg="#1e1f21", bd=0, highlightthickness=0)
        self.canvas_1.grid(row=0, column=0)
        # other canvas for other oppents
        self.canvas_2 = Canvas(self, width=self.w, height=self.h, bg="#1e1f21", bd=0, highlightthickness=0)
        self.canvas_2.grid(row=0, column=1)

        # create Score canvases
        self.canvas_score_1 = Canvas(self, width=self.w, height="200", bg="black", bd=0, highlightthickness=0)
        self.canvas_score_1.grid(row=1, column=0)
        self.canvas_score_2 = Canvas(self, width=self.w, height="200", bg="black", bd=0, highlightthickness=0)
        self.canvas_score_2.grid(row=1, column=1)

        # create the rectangle 
        # self.canvas_score_1.create_polygon(10, 10, 20, 0, self.w-20, 0, self.w-10, 10, self.w, 20, self.w, 200, 0, 200, fill="red", smooth=True)

        self.t = 25
        self.n = 10
        self.R = 0.7* (self.w-self.t*2)/(self.n*2)
        # defined the colors
        self.black_color = "black"
        self.white_color = "white"
        # create the Dam board
        
        self.create_DamBoard()

        # load the chessman images
        self.redman = ImageTk.PhotoImage(Image.open("red_chessman.png").resize((int(self.R*2), int(self.R*2))))
        self.blueman = ImageTk.PhotoImage(Image.open("blue_chessman.png").resize((int(self.R * 2), int(self.R*2))))
        # load the image for kings of partners
        self.blueking = ImageTk.PhotoImage(Image.open("king chessmans/blue_king.png").resize((int(self.R*2), int(self.R*2))))
        self.redking = ImageTk.PhotoImage(Image.open("king chessmans/red_king.png").resize((int(self.R * 2), int(self.R*2))))


        # create the New Game
        self.New_Game()

        # binding the canvas_1 and canvas_2
        self.canvas_1.bind("<Button-1>", self.get_disk)
        self.canvas_1.bind("<Motion>", self.box_highlight)
        self.canvas_1.bind("<B1-Motion>", self.motined_disk)
        self.canvas_1.bind("<ButtonRelease>", self.getAction)

        self.canvas_2.bind("<Button-1>", self.get_disk2)
        self.canvas_2.bind("<Motion>", self.box_highlight)
        self.canvas_2.bind("<B1-Motion>", self.motined_disk2)
        self.canvas_2.bind("<ButtonRelease>", self.getAction2)






    def create_DamBoard(self):
        """
        draw the Dam board on the canvas

        """

        color = self.white_color
        w = (self.w-2*self.t)/self.n
        for j in range(0, self.n):
            for i in range(0, self.n):
                self.canvas_1.create_rectangle(self.t + i*w, self.t + j*w, self.t + (i+1)*w, self.t + (j+1)*w, fill=color, outline=color)
                self.canvas_2.create_rectangle(self.t + i * w, self.t + j * w, self.t + (i + 1) * w, self.t + (j + 1) * w, fill=color, outline=color)
                if i != self.n-1:
                    if color == self.black_color:
                        color = self.white_color
                    else:
                        color = self.black_color

    def New_Game(self):
        
        self.number_of_disks = 16
        # create the empty partners
        self.partner_1 = {}
        self.partner_2 = {}
        # create the kings list of the partners
        self.partner_1_kings = {}
        self.partner_2_kings = {}
        # count of the kings
        self.kings_1 = 0
        self.kings_2 = 0
        self.clicked_king_tag = False
        # create var to get number of removed disks
        self.count_removeDisk1 = 0
        self.count_removeDisk2 = 0
        # defined the new var 
        self.side = random.choice([1,2])
        self.clicked_disk = False

        # set the initial position of the disks
        for partner in (self.partner_1, self.partner_2):
            n = 1
            for j in range(0, 3):
                for i in range(0, self.n):
                    partner[f"{n}"] = {"i" : i,
                                        "j" : j}
                    n += 1


        # set the Dam board for disks current positions
        self.canvas_1.delete(ALL)
        self.canvas_2.delete(ALL)
        self.create_DamBoard()
        self.set_board()
        # update the scores
        self.update_scores()
        # display the active partner
        self.display_active_partner()

    def set_board(self):

        w = (self.w - 2 * self.t) / self.n
        # set the first board
        # for partner 1
        for item in self.partner_1.keys():
            i, j = self.partner_1[item]["i"], self.partner_1[item]["j"]
            # calculate the disk center
            ox, oy = self.t + i*w + w/2 , self.h - (self.t + j*w) - w/2
            self.canvas_1.create_image(ox, oy, image=self.redman, tag=F"{item}|1")

            # create this disk for partner 2 board
            new_i , new_j = self.n-1-i, self.n-1-j
            new_ox, new_oy = self.t + new_i*w + w/2 , self.h - (self.t + new_j*w) - w/2
            self.canvas_2.create_image(new_ox, new_oy, image=self.redman, tag=f"{item}|1")


        for item in self.partner_2.keys():
            i, j = self.partner_2[item]["i"], self.partner_2[item]["j"]
            # calculate the disk center
            ox, oy = self.t + i * w + w / 2, self.h - (self.t + j * w) - w / 2
            self.canvas_2.create_image(ox, oy, image=self.blueman, tag=f"{item}|2")

            # create this disk for partner 2 board
            new_i, new_j = self.n - 1 - i, self.n - 1 - j
            new_ox, new_oy = self.t + new_i * w + w / 2, self.h - (self.t + new_j * w) - w / 2
            self.canvas_1.create_image(new_ox, new_oy, image=self.blueman ,tag=f"{item}|2")
        
        # create hte kings chessman in the Dam board
        if self.partner_1_kings != {}:
            for king in self.partner_1_kings.keys():
                i, j = self.partner_1_kings[king]["i"], self.partner_1_kings[king]["j"]
                # calculate the disk center
                ox, oy = self.t + i * w + w / 2, self.h - (self.t + j * w) - w / 2
                self.canvas_1.create_image(ox, oy, image=self.redking, tag=f"{king}|1K")

                # create this disk for partner 2 board
                new_i, new_j = self.n - 1 - i, self.n - 1 - j
                new_ox, new_oy = self.t + new_i * w + w / 2, self.h - (self.t + new_j * w) - w / 2
                self.canvas_2.create_image(new_ox, new_oy, image=self.redking ,tag=f"{king}|1K")

        if self.partner_2_kings != {}:
            for king in self.partner_2_kings.keys():
                i, j = self.partner_2_kings[king]["i"], self.partner_2_kings[king]["j"]
                # calculate the disk center
                ox, oy = self.t + i * w + w / 2, self.h - (self.t + j * w) - w / 2
                self.canvas_2.create_image(ox, oy, image=self.blueking, tag=f"{king}|2K")

                # create this disk for partner 2 board
                new_i, new_j = self.n - 1 - i, self.n - 1 - j
                new_ox, new_oy = self.t + new_i * w + w / 2, self.h - (self.t + new_j * w) - w / 2
                self.canvas_1.create_image(new_ox, new_oy, image=self.blueking ,tag=f"{king}|2K")


    def set_newPosition(self, id, new_i, new_j):

        w = (self.w - 2 * self.t) / self.n
        # get info about disk
        split_str = list(id.split("|"))
        partner , number = split_str[1], int(split_str[0])
        # first delete the disk in the previous position
        self.canvas_1.delete(id)
        self.canvas_2.delete(id)

        if partner == "1" or partner == "1K":

            # now create the new disk in the currrent new position
            new_ox, new_oy = self.t + new_i * w + w / 2, self.h - (self.t + new_j * w) - w / 2
            if partner == "1":
                self.canvas_1.create_image(new_ox ,new_oy, image=self.redman, tag=id)
            elif partner == "1K":
                self.canvas_1.create_image(new_ox ,new_oy, image=self.redking, tag=id)

            inv_new_ox, inv_new_oy = self.t + (self.n-1-new_i) * w + w / 2, self.h - (self.t + (self.n-1-new_j) * w) - w / 2
            if partner == "1":
                self.canvas_2.create_image(inv_new_ox, inv_new_oy, image=self.redman, tag=id)
            elif partner == "1K":
                self.canvas_2.create_image(inv_new_ox, inv_new_oy, image=self.redking, tag=id)


            # set the new position to partner_2 dict
            if partner == "1":
                self.partner_1[f"{number}"]["i"] = new_i
                self.partner_1[f"{number}"]["j"] = new_j
            elif partner == "1K":
                self.partner_1_kings[f"{number}"]["i"] = new_i
                self.partner_1_kings[f"{number}"]["j"] = new_j


        elif partner == "2" or partner == "2K":

            # now create the new disk in the currrent new position
            new_ox, new_oy = self.t + new_i * w + w / 2, self.h - (self.t + new_j * w) - w / 2
            if partner == "2":
                self.canvas_2.create_image(new_ox, new_oy, image=self.blueman, tag=id)
            elif partner == "2K":
                self.canvas_2.create_image(new_ox, new_oy, image=self.blueking, tag=id)

            inv_new_ox, inv_new_oy = self.t + (self.n - 1 - new_i) * w + w / 2, self.h - (
                        self.t + (self.n - 1 - new_j) * w) - w / 2
            if partner == "2":
                self.canvas_1.create_image(inv_new_ox, inv_new_oy, image=self.blueman, tag=id)
            elif partner == "2K":
                self.canvas_1.create_image(inv_new_ox, inv_new_oy, image=self.blueking, tag=id)

            # set the new position to partner_2 dict
            if partner == "2":
                self.partner_2[f"{number}"]["i"] = new_i
                self.partner_2[f"{number}"]["j"] = new_j
            elif partner == "2K":
                self.partner_2_kings[f"{number}"]["i"] = new_i
                self.partner_2_kings[f"{number}"]["j"] = new_j

        self.check_for_availableOfKings()


    def check_for_availableOfKings(self):

        # check first the available of kings of partner_1
        for key in self.partner_1.keys():
            if self.partner_1[key]["j"] == self.n - 1:
                self.kings_1 += 1
                self.partner_1_kings[f"{self.kings_1}"] = {"i" : self.partner_1[key]["i"],
                                                            "j" : self.partner_1[key]["j"]}
                self.partner_1.pop(key)
                self.set_board()
                break


        # check first the available of kings of partner_2
        for key in self.partner_2.keys():
            if self.partner_2[key]["j"] == self.n - 1:
                self.kings_2 += 1
                self.partner_2_kings[f"{self.kings_2}"] = {"i" : self.partner_2[key]["i"],
                                                            "j" : self.partner_2[key]["j"]}
                self.partner_2.pop(key)
                self.set_board()
                break

    def get_disk(self, event):

        w = (self.w - 2 * self.t) / self.n

        if self.side == 1:

            # first get the clicked disk info
            clicked_obj = self.canvas_1.find_closest(event.x, event.y)[0]
            clicked_tag = self.canvas_1.gettags(clicked_obj)[0]

            if "|" in clicked_tag and not("K" in clicked_tag):
                split_str = clicked_tag.split("|")
                self.clicked_disk = [int(split_str[1]), int(split_str[0])]
            else:
                self.clicked_disk = False
            # check for kings
            if "|" in clicked_tag and ("K" in clicked_tag):
                split_str = clicked_tag.split("|")
                self.clicked_king_tag = [split_str[1] , int(split_str[0])]
            else:
                self.clicked_king_tag = False

            # then highlight the clicked box
            i, j = int((event.x-self.t)/w) , int((self.h-event.y-self.t)/w)
            if 0 <= i <= self.n and 0 <= j <= self.n :
                self.highlight_box(i, j, 1)

    def get_disk2(self, event):

        w = (self.w - 2 * self.t) / self.n

        if self.side == 2:
            # first get the clicked disk info
            clicked_obj = self.canvas_2.find_closest(event.x, event.y)[0]
            clicked_tag = self.canvas_2.gettags(clicked_obj)[0]

            if "|" in clicked_tag and not("K" in clicked_tag):
                split_str = clicked_tag.split("|")
                self.clicked_disk = [int(split_str[1]), int(split_str[0])]
            else:
                self.clicked_disk = False

            # check for kings
            if "|" in clicked_tag and ("K" in clicked_tag):
                split_str = clicked_tag.split("|")
                self.clicked_king_tag = [split_str[1] , int(split_str[0])]
            else:
                self.clicked_king_tag = False

            # then highlight the clicked box
            i, j = int((event.x-self.t)/w) , int((self.h-event.y-self.t)/w)
            if 0 <= i <= self.n and 0 <= j <= self.n :
                self.highlight_box(i, j, 2)

    def getAction(self, event):

        w = (self.w - 2 * self.t) / self.n
        if self.clicked_disk and self.side == 1:
            # get the new i and j
            mi, mj = int((event.x-self.t)/w) , int((self.h-event.y-self.t)/w)
            # disk move to new position
            if self.check_validity(self.clicked_disk, mi, mj):
                self.set_newPosition(f"{self.clicked_disk[1]}|{self.clicked_disk[0]}", mi, mj)
                #   delete the highligth box
                self.canvas_1.delete("highlight_line")
                self.canvas_2.delete("highlight_line")
            else:
                self.canvas_1.delete(ALL)
                self.canvas_2.delete(ALL)
                self.create_DamBoard()
                self.set_board()

            # display the active partner
            self.display_active_partner()

        elif self.clicked_king_tag and self.side == 1:
            # get the new i and j
            mi, mj = int((event.x-self.t)/w) , int((self.h-event.y-self.t)/w)
            if self.check_validity_for_kings(self.clicked_king_tag, mi, mj):
                self.set_newPosition(f"{self.clicked_king_tag[1]}|{self.clicked_king_tag[0]}", mi, mj)
                self.canvas_1.delete("highlight_line")
                self.canvas_2.delete("highlight_line")

            else:
                self.canvas_1.delete(ALL)
                self.canvas_2.delete(ALL)
                self.create_DamBoard()
                self.set_board()



            # display the active partner
            self.display_active_partner()

    def getAction2(self, event):

        w = (self.w - 2 * self.t) / self.n
        if self.clicked_disk and self.side == 2:
            # get the new i and j
            mi, mj = int((event.x-self.t)/w) , int((self.h-event.y-self.t)/w)
            # disk move to new position
            if self.check_validity(self.clicked_disk, mi, mj):
                self.set_newPosition(f"{self.clicked_disk[1]}|{self.clicked_disk[0]}", mi, mj)
                # delete the highlight box
                self.canvas_1.delete("highlight_line")
                self.canvas_2.delete("highlight_line")


            else:
                self.canvas_1.delete(ALL)
                self.canvas_2.delete(ALL)
                self.create_DamBoard()
                self.set_board()

            # display the active partner
            self.display_active_partner()

        elif self.clicked_king_tag and self.side == 2:
            # get the new i and j
            mi, mj = int((event.x-self.t)/w) , int((self.h-event.y-self.t)/w)
            if self.check_validity_for_kings(self.clicked_king_tag, mi, mj):
                self.set_newPosition(f"{self.clicked_king_tag[1]}|{self.clicked_king_tag[0]}", mi, mj)
                self.canvas_1.delete("highlight_line")
                self.canvas_2.delete("highlight_line")

            else:
                self.canvas_1.delete(ALL)
                self.canvas_2.delete(ALL)
                self.create_DamBoard()
                self.set_board()



            # display the active partner
            self.display_active_partner()

    def check_validity_for_kings(self, king_tag, i, j):
        
        # get the disk current data
        if king_tag[0] == "1K":
            current_i, current_j = self.partner_1_kings[f"{king_tag[1]}"]["i"], self.partner_1_kings[f"{king_tag[1]}"]["j"]
        elif king_tag[0] == "2K":
            current_i, current_j = self.partner_2_kings[f"{king_tag[1]}"]["i"], self.partner_2_kings[f"{king_tag[1]}"]["j"]

        if self.check_indisk(king_tag[0], i, j):
            if self.check_validity_of_position(king_tag, i, j, current_i, current_j):
                return True

    def check_validity_of_position(self, tag, new_i, new_j, current_i, current_j):
        
        # take proceed
        checked_list = self.generate_internal_list(current_i, current_j ,new_i, new_j)
        t = True
        if tag[0] == "1K":
            for l in self.partner_1.keys():
                if [self.partner_1[l]["i"], self.partner_1[l]["j"]] in checked_list:
                    t = False
                    break
            for l in self.partner_1_kings.keys():
                if [self.partner_1_kings[l]["i"], self.partner_1_kings[l]["j"]] in checked_list:
                    t = False
                    break

        if tag[0] == "2K":
            for l in self.partner_2.keys():
                if [self.partner_2[l]["i"], self.partner_2[l]["j"]] in checked_list:
                    t = False
                    break
            for l in self.partner_2_kings.keys():
                if [self.partner_2_kings[l]["i"], self.partner_2_kings[l]["j"]] in checked_list:
                    t = False
                    break

        if t and abs(new_i - current_i) == abs(new_j - current_j):
            if not self.check_for_remove_ByKings(tag, current_i, current_j, new_i, new_j):
                # change the side
                if self.side == 1:
                    self.side = 2
                else:
                    self.side = 1
            return True

    def generate_internal_list(self, i, j ,new_i, new_j):

        # return the all posible coordinates in the range of king path
        l = []
        # first detect the direction
        if (new_i > i and new_j > j):
            direction = 1
        elif (new_i < i and new_j > j):
            direction = 2
        elif (new_i < i and new_j < j):
            direction = 3
        else:
            direction = 4
        # now generate the list
        for k in range(1, abs(new_i - i)):
            if direction == 1:
                l.append([i + k, j + k])
            elif direction == 2:
                l.append([i - k, j + k])
            elif direction == 3:
                l.append([i - k, j - k])
            else:
                l.append([i + k, j - k])

        return l

    def check_validity(self, info, new_i, new_j):
        # get the disk current data
        if info[0] == 1:
            current_i, current_j = self.partner_1[f"{info[1]}"]["i"], self.partner_1[f"{info[1]}"]["j"]
        elif info[0] == 2:
            current_i, current_j = self.partner_2[f"{info[1]}"]["i"], self.partner_2[f"{info[1]}"]["j"]

        # chec the validity
        if self.check_indisk(info[0], new_i, new_j):
            if (new_i == current_i +1 and new_j == current_j +1) or (new_i == current_i-1 and new_j == current_j + 1):
                # set the appropriate side
                if self.side == 1:
                    self.side = 2
                elif self.side == 2:
                    self.side = 1
                return  True

            elif (new_i == current_i + 2 and new_j == current_j + 2):
                if self.check_for_remove(info[0], current_i+1, current_j+1):
                    return  True
            elif (new_i == current_i - 2 and new_j == current_j + 2):
                if self.check_for_remove(info[0], current_i-1, current_j+1):
                    return  True


    def check_indisk(self, id, checked_i, checked_j):
        # get the i, j info to list
        disk_list = []
        if id == 1 or id == "1K":
            for i in self.partner_1.keys():
                disk_list.append([self.partner_1[i]["i"], self.partner_1[i]["j"]])
            # then get the ondo about the partner 2
            for k in self.partner_2.keys():
                disk_list.append([self.n - 1 - self.partner_2[k]["i"], self.n - 1 - self.partner_2[k]["j"]])
            if self.partner_1_kings != {}:
                for i in self.partner_1_kings.keys():
                    disk_list.append([self.partner_1_kings[i]["i"], self.partner_1_kings[i]["j"]])
            if self.partner_2_kings != {}: 
                # then get the ondo about the partner 2
                for k in self.partner_2_kings.keys():
                    disk_list.append([self.n - 1 - self.partner_2_kings[k]["i"], self.n - 1 - self.partner_2_kings[k]["j"]])

        elif id == 2 or id == "2K":
            for i in self.partner_2.keys():
                disk_list.append([self.partner_2[i]["i"], self.partner_2[i]["j"]])
            # then get the ondo about the partner 2
            for k in self.partner_1.keys():
                disk_list.append([self.n - 1 - self.partner_1[k]["i"], self.n - 1 - self.partner_1[k]["j"]])

            if self.partner_2_kings != {}: 
                for i in self.partner_2_kings.keys():
                    disk_list.append([self.partner_2_kings[i]["i"], self.partner_2_kings[i]["j"]])
            # then get the ondo about the partner 2
            if self.partner_1_kings != {}:
                for k in self.partner_1_kings.keys():
                    disk_list.append([self.n - 1 - self.partner_1_kings[k]["i"], self.n - 1 - self.partner_1_kings[k]["j"]])

        # check validity
        if [checked_i, checked_j ] in disk_list:
            return False
        else:
            return  True

    def check_for_remove(self, id, checked_i, checked_j):

        if id == 1:
            # get the detail of partner to the list
            for i in self.partner_2.keys():
                if [checked_i, checked_j] == [self.n - 1 - self.partner_2[i]["i"], self.n - 1 - self.partner_2[i]["j"]]:
                    self.remove_disk(2, i)
                    return   True
                    break

            for k in self.partner_2_kings.keys():
                if [checked_i, checked_j] == [self.n - self.partner_2_kings[k]["i"], self.n-1-self.partner_2_kings[k]['j']]:
                    self.remove_disk("2k", k)
                    return True
                    break



        if id == 2:
            # get the info about the partner_2
            for i in self.partner_1.keys():
                if [checked_i, checked_j] == [self.n - 1 - self.partner_1[i]["i"], self.n - 1 - self.partner_1[i]["j"]]:
                    self.remove_disk(1, i)
                    return  True
                    break

            for k in self.partner_1_kings.keys():
                if [checked_i, checked_j] == [self.n - self.partner_1_kings[k]["i"], self.n-1-self.partner_1_kings[k]['j']]:
                    self.remove_disk("1k", k)
                    return True
                    break


    def check_for_remove_ByKings(self, tag, i, j, new_i, new_j):

        checked_list = self.generate_internal_list(i, j, new_i, new_j)
        remove_normal = []
        remove_kings = []

        if tag[0] == "1K":
            for k in self.partner_2.keys():
                if [self.n- 1 -self.partner_2[k]["i"], self.n - 1 - self.partner_2[k]["j"]] in checked_list:
                    remove_normal.append([2, k])
            for k in self.partner_2_kings.keys():
                if [self.n- 1 - self.partner_2_kings[k]["i"], self.n - 1 - self.partner_2_kings[k]["j"]] in checked_list:
                    remove_kings.append([2, k])

        elif tag[0] == "2K":
            for k in self.partner_1.keys():
                if [self.n- 1 -self.partner_1[k]["i"], self.n - 1 - self.partner_1[k]["j"]] in checked_list:
                    remove_normal.append([1, k])
            for k in self.partner_1_kings.keys():
                if [self.n- 1 - self.partner_1_kings[k]["i"], self.n - 1 - self.partner_1_kings[k]["j"]] in checked_list:
                    remove_kings.append([1, k])

        total_removed_disks = [remove_normal, remove_kings]
        self.cleanup_disks(total_removed_disks)
        
        if remove_normal != [] or remove_kings != []:
            return True
        else:
            return False

    def cleanup_disks(self, removed_disks):

        self.canvas_1.delete(ALL)
        self.canvas_2.delete(ALL)
        self.create_DamBoard()

        for d in removed_disks[0]:
            if d[0] == 1:
                self.partner_1.pop(f"{d[1]}")
                self.count_removeDisk1 += 1
            elif d[0] == 2:
                self.partner_2.pop(f"{d[1]}")
                self.count_removeDisk2 += 1

        for e in removed_disks[1]:
            if e[0] == 1:
                self.partner_1_kings.pop(f"{e[1]}")
                self.count_removeDisk1 += 1
            elif e[0] == 2:
                self.partner_2_kings.pop(f"{e[1]}")
                self.count_removeDisk2 += 1

        self.set_board()
        self.update_scores()

    def remove_disk(self, id, key):

        #forst remove all of dis from the both boards
        self.canvas_1.delete(ALL)
        self.canvas_2.delete(ALL)
        self.create_DamBoard()
        if id == 1:
            self.partner_1.pop(f"{key}")
            self.set_board()
            self.count_removeDisk1 +=  1
        elif id  == 2:
            self.partner_2.pop(f"{key}")
            self.set_board()
            self.count_removeDisk2 += 1
        elif id == "1k":
            self.partner_1_kings.pop(f"{key}")
            self.set_board()
            self.count_removeDisk1 += 1
        elif id == "2k":
            self.partner_2_kings.pop(f"{key}")
            self.set_board()
            self.count_removeDisk2 += 1
        # update the scores
        self.update_scores()

    def update_scores(self):

        self.canvas_score_1.delete(ALL)
        self.canvas_score_2.delete(ALL)
        # first update the canvas_1 scores
        available_disks1 = len(self.partner_1.keys())

        self.display_removed_disks()

        self.canvas_score_1.create_text(self.w*0.2, 150, text=f"available : {available_disks1}", fill="white", font=('Helvetica', 10), tag="scores")
        self.canvas_score_1.create_text(self.w*0.4, 150, text=f"removed : {self.count_removeDisk1}", fill="white", font=('Helvetica', 10), tag="scores")

        # now update the canvas_2 scores
        available_disks2 = len(self.partner_2.keys())

        self.canvas_score_2.create_text(self.w*0.2, 150, text=f"available : {available_disks2}", fill="white",
                                        font=('Helvetica', 10), tag="scores")
        self.canvas_score_2.create_text(self.w * 0.4, 150, text=f"removed : {self.count_removeDisk2}", fill="white",
                                        font=('Helvetica', 10), tag="scores")


    def display_removed_disks(self):
        # display the removed diks by draw the disks

        # display the removed disks in the canvas_1
        d = (self.w - 2*self.t) / self.n
        i = 0
        while i <= self.count_removeDisk1:
            for k in range(0, 3):
                for j in range(0, int(self.w/d) - 1):
                    i += 1
                    if i > self.count_removeDisk1:
                        break
                    self.canvas_score_1.create_image(d + j*d, d+ k*d, image=self.redman)

        # display the removed disk in the canvas_2
        i = 0
        while i <= self.count_removeDisk2:
            for k in range(0, 3):
                for j in range(0, int(self.w/d)-1):
                    i += 1
                    if i > self.count_removeDisk2:
                        break
                    self.canvas_score_2.create_image(d + j*d, d+ k*d, image=self.blueman)



    def motined_disk(self, event):

        if self.clicked_disk and self.side == 1:
            if self.clicked_disk[0] == 1:
                self.canvas_1.delete(f"{self.clicked_disk[1]}|1")
                self.canvas_2.delete(f"{self.clicked_disk[1]}|1")
                self.canvas_1.create_image(event.x, event.y, image=self.redman, tag=f"{self.clicked_disk[1]}|1")
                self.canvas_2.create_image(self.w-event.x, self.h-event.y, image=self.redman, tag=f"{self.clicked_disk[1]}|1")

    def motined_disk2(self, event):

        if self.clicked_disk and self.side == 2:
            if self.clicked_disk[0] == 2:
                self.canvas_1.delete(f"{self.clicked_disk[1]}|2")
                self.canvas_2.delete(f"{self.clicked_disk[1]}|2")
                self.canvas_2.create_image(event.x, event.y, image=self.blueman, tag=f"{self.clicked_disk[1]}|2")
                self.canvas_1.create_image(self.w - event.x, self.h - event.y, image=self.blueman,
                                           tag=f"{self.clicked_disk[1]}|2")


    def highlight_box(self, i, j, id):

        w = (self.w - 2 * self.t) / self.n
        
        self.canvas_1.delete("highlight_line")
        self.canvas_2.delete("highlight_line")

        if id == 1:
            # highlight the partner 1 (i, j) box
            # draw the border of the clicked box
            self.canvas_1.create_rectangle(self.t + i*w, self.h-(self.t + w*j), self.t + (i+1)*w, self.h-(self.t + (j+1)*w), fill=None, outline="red", width="2", tag="highlight_line")
            inv_i, inv_j = self.n-1-i, self.n-1-j
            self.canvas_2.create_rectangle(self.t + inv_i*w, self.h-(self.t + w*inv_j), self.t + (inv_i+1)*w, self.h-(self.t + (inv_j+1)*w), fill=None, outline="red", width="2", tag="highlight_line")

        elif id == 2:
            # highlight the partner 1 (i, j) box
            # draw the border of the clicked box 
            self.canvas_2.create_rectangle(self.t + i*w, self.h-(self.t + w*j), self.t + (i+1)*w, self.h-(self.t + (j+1)*w), fill=None, outline="red", width="2", tag="highlight_line")
            inv_i, inv_j = self.n-1-i, self.n-1-j
            self.canvas_1.create_rectangle(self.t + inv_i*w, self.h-(self.t + w*inv_j), self.t + (inv_i+1)*w, self.h-(self.t + (inv_j+1)*w), fill=None, outline="red", width="2", tag="highlight_line")

    def display_active_partner(self):

        self.canvas_1.delete("active_box")
        self.canvas_2.delete("active_box")
        if self.side == 1:
            self.canvas_1.create_rectangle(self.t, self.t, self.w-self.t, self.h-self.t, fill=None, outline="green2", width="5", tag="active_box")
            self.canvas_2.create_rectangle(self.t, self.t, self.w-self.t, self.h-self.t, fill=None, outline="red2", width="5", tag="active_box")
            # change color of the text
            self.canvas_score_1.itemconfigure("scores", fill="green2")
            self.canvas_score_2.itemconfigure("scores", fill="red")

            self.canvas_1.config(bg="green2")
            self.canvas_2.config(bg="red")
        else:
            self.canvas_1.create_rectangle(self.t, self.t, self.w-self.t, self.h-self.t, fill=None, outline="red2", width="5", tag="active_box")
            self.canvas_2.create_rectangle(self.t, self.t, self.w-self.t, self.h-self.t, fill=None, outline="green2", width="5", tag="active_box")
             # change color of the text
            self.canvas_score_2.itemconfigure("scores", fill="green2")
            self.canvas_score_1.itemconfigure("scores", fill="red")
            #
            self.canvas_1.config(bg="red")
            self.canvas_2.config(bg="green2")
    
    def box_highlight(self, event):

        w = (self.w-2*self.t)/self.n
        self.canvas_1.delete("box")
        self.canvas_2.delete("box")
        self.canvas_score_1.delete("box")
        self.canvas_score_2.delete("box")
        mi, mj = int((event.x-self.t)/w) , int((self.h-event.y-self.t)/w)
        
        if self.side == 1:
            if 0 <= mi < self.n and 0 <= mj < self.n:
                self.canvas_1.create_rectangle(self.t + w*mi, self.h - (self.t + mj*w), self.t + (mi+1)*w, self.h-(self.t + (mj+1)*w), fill=None, outline="yellow", tag="box")
                self.canvas_score_1.create_text(self.w*0.2, 170, text=f"i   :   {mi}", fill="white", tag="box")
                self.canvas_score_1.create_text(self.w*0.2, 190, text=f"j   :   {mj}", fill="white", tag="box")
        
        elif self.side == 2:
            if 0 <= mi < self.n and 0 <= mj < self.n:
                self.canvas_2.create_rectangle(self.t + w*mi, self.h - (self.t + mj*w), self.t + (mi+1)*w, self.h-(self.t + (mj+1)*w), fill=None, outline="yellow", tag="box")
                self.canvas_score_2.create_text(self.w*0.2, 170, text=f"i   :   {mi}", fill="white", tag="box")
                self.canvas_score_2.create_text(self.w*0.2, 190, text=f"j   :   {mj}", fill="white", tag="box")

    def change_color(self, color_type):

        # ask color from the color chooser
        changed_color = colorchooser.askcolor()[1]
        if color_type == "black":
            self.black_color = changed_color
        else:
            self.white_color = changed_color

        # update the bot canvases
        self.canvas_1.delete(ALL)
        self.canvas_2.delete(ALL)
        self.create_DamBoard()
        self.set_board()
        self.display_active_partner()

if __name__ == "__main__":
    DamGame().mainloop()
