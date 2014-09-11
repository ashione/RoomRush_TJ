#!/usr/bin/python
import pthread
import roomRush
def main():
	myRoomRush =roomRush.RoomRush()	
	myRoomRush.loadData()
	if myRoomRush.login() :

		raw_input('input anything start \n')
		myThread1 = pthread.Pthread(myRoomRush)
		myThread2 = pthread.Pthread(myRoomRush)
		myThread3 = pthread.Pthread(myRoomRush)
		myThread4 = pthread.Pthread(myRoomRush)
		myThread1.start()
		myThread2.start()
		myThread3.start()
		myThread4.start()
if __name__ == '__main__':
	main()
