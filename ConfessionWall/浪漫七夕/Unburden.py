# Python表白脚本
import pygame
import random
import time
import turtle
import multiprocessing


def music_play():
	pygame.mixer.init()
	while True:
		music_name = str(random.randint(1, 3)) + '.mp3'
		pygame.mixer.music.load('./music/%s' % music_name)
		pygame.mixer.music.play(start=1.0)
		time.sleep(120)
		pygame.mixer.music.stop()


def draw_arc(lv):
	for i in range(20):
		lv.right(10)
		lv.forward(2)


def draw_love(x, y):
	love = turtle.Turtle()
	love.hideturtle()
	love.up()
	love.goto(x, y)
	love.color('red', 'pink')
	love.speed(10000000)
	love.pensize(2)
	love.down()
	love.begin_fill()
	love.left(140)
	love.forward(22)
	draw_arc(love)
	love.left(120)
	draw_arc(love)
	love.forward(22)
	love.left(140)
	love.end_fill()


def draw_tree(branchLen, tur):
	if branchLen > 5:
		if branchLen < 20:
			tur.color('green')
			tur.pensize(random.uniform((branchLen+5)/4-2, (branchLen+6)/4+5))
			tur.down()
			tur.forward(branchLen)
			draw_love(tur.xcor(), tur.ycor())
			tur.up()
			tur.backward(branchLen)
			tur.color('brown')
			return
		tur.pensize(random.uniform((branchLen+5)/4-2, (branchLen+6)/4+5))
		tur.down()
		tur.forward(branchLen)
		angle = random.uniform(15, 45)
		tur.right(angle)
		draw_tree(branchLen-random.uniform(12, 16), tur)
		tur.left(2*angle)
		draw_tree(branchLen-random.uniform(12, 16), tur)
		tur.right(angle)
		tur.up()
		tur.backward(branchLen)


def draw_main():
	Win = turtle
	tur = turtle.Turtle()
	tur.hideturtle()
	tur.speed(1000)
	tur.left(90)
	tur.up()
	tur.backward(200)
	tur.down()
	tur.color("brown")
	tur.pensize(32)
	tur.forward(60)
	draw_tree(100, tur)
	Win.exitonclick()


if __name__ == '__main__':
	process1 = multiprocessing.Process(target=draw_main)
	process2 = multiprocessing.Process(target=music_play)
	process1.start()
	process2.start()