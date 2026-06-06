import turtle 
import time
import random
import winsound  # Menggunakan winsound standar Windows

# --- 1. Struktur Data Doubly Linked List ---
class Node:
    def __init__(self, obj):
        self.obj = obj  
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0 

    def add(self, obj):
        new_node = Node(obj)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.count += 1
        return new_node

    def remove(self, node):
        if not node: return
        node.obj.hideturtle()  
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self.count -= 1

    def clear_all(self):
        """Menghapus semua node dan menyembunyikan turtle-nya."""
        curr = self.head
        while curr:
            curr.obj.hideturtle()
            curr = curr.next
        self.head = None
        self.tail = None
        self.count = 0

# --- 2. Setup Layar Utama ---
screen = turtle.Screen()
screen.title("Space Shooter DLL - Fixed Sound Edition")
screen.bgcolor("#1a1a1a")
screen.setup(width=600, height=600)
screen.tracer(0)

# Global variables untuk kontrol
bullet_list = DoublyLinkedList()
enemy_list = DoublyLinkedList()
score = 0

# Papan Skor
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()

def update_score():
    pen.clear()
    pen.goto(0, 260)
    pen.write(f"Skor: {score}", align="center", font=("Courier", 24, "bold"))

# Pemain
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.setheading(90)

# Kontrol Pemain
def move_left():
    if player.xcor() > -280: player.setx(player.xcor() - 25)

def move_right():
    if player.xcor() < 280: player.setx(player.xcor() + 25)

def fire():
    if bullet_list.count < 5: 
        b = turtle.Turtle()
        b.shape("square")
        b.color("yellow")
        b.shapesize(0.2, 0.5)
        b.penup()
        b.goto(player.xcor(), player.ycor() + 20)
        b.setheading(90)
        bullet_list.add(b)
        
        # Menggunakan suara sistem Windows (tidak membuat game lag/macet)
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)

screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(fire, "space")

# --- 3. Fungsi Logika Game Utama ---
def play_game():
    global score
    # Reset Kondisi Awal
    score = 0
    bullet_list.clear_all()
    enemy_list.clear_all()
    player.goto(0, -250)
    update_score()
    
    game_running = True
    while game_running:
        screen.update()
        time.sleep(0.01)

        # Spawn Musuh
        if random.randint(1, 60) == 1 and enemy_list.count < 3: 
            e = turtle.Turtle()
            e.shape("circle")
            e.color("red")
            e.penup()
            e.goto(random.randint(-280, 280), 280)
            enemy_list.add(e)

        # Pergerakan Peluru
        curr_b = bullet_list.head
        while curr_b:
            next_b = curr_b.next
            curr_b.obj.forward(10)
            if curr_b.obj.ycor() > 300:
                bullet_list.remove(curr_b)
            curr_b = next_b

        # Pergerakan Musuh & Collision
        curr_e = enemy_list.head
        while curr_e:
            next_e = curr_e.next
            curr_e.obj.sety(curr_e.obj.ycor() - 2)

            # Cek Tabrakan dengan Peluru
            curr_b = bullet_list.head
            while curr_b:
                next_b = curr_b.next
                if curr_e.obj.distance(curr_b.obj) < 20:
                    bullet_list.remove(curr_b)
                    enemy_list.remove(curr_e)
                    score += 1
                    update_score()
                    
                    # Suara ledakan musuh menggunakan suara notifikasi Windows
                    winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
                    break 
                curr_b = next_b

            # Jika musuh lewat atau kena pemain
            if curr_e:
                if curr_e.obj.ycor() < -300:
                    enemy_list.remove(curr_e)
                elif curr_e.obj.distance(player) < 25:
                    # Suara Game Over
                    winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
                    game_running = False 
            
            curr_e = next_e

    # --- 4. Proses Game Over ---
    pen.goto(0, 0)
    pen.write("GAME OVER\nMemuat Ulang...", align="center", font=("Courier", 30, "bold"))
    screen.update()
    time.sleep(3) 
    pen.clear()

# --- 5. Loop Utama Aplikasi ---
if __name__ == "__main__":
    while True:
        play_game()