#####
#
#     ASK/FALSK APi for using Alexa to interface with an mBot Device
#     By: Dr. Edwin A Hernandez   edwinhm@eglacorp.com
#     (C) 2017   - EGLA COMMUNICATIONS  - All rights reserved
#
#######################@

from random    import randint
from flask     import Flask, render_template, g
from flask_ask import Ask, statement, question, session
import logging
from lib.mBot import *

app      = Flask(__name__)
ask      = Ask(app, "/")
STEPS    = 0.2
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


bot          = None;
nCollisions  = 0;
heading      = "forward"

def initMBot():
    bot = mBot()
    bot.startWithSerial("/dev/tty.Makeblock-ELETSPP")
    return bot;

def onDistanceForward(dist):
  global bot;
  global nCollisions

  print "Forward ... Forward ... "
  print "distance:",dist

  if dist<20 :
      bot.doMove(-100,-100)
      sleep(0.5)
      bot.doMove(100,-100)
      sleep(0.1)
      nCollisions = nCollisions  + 1
      #session.attributes["collisions"] = nCollisions
  bot.doMove(100,100)
  sleep(STEPS)

def onDistanceBackward(dist):
  global bot
  global nCollisions

  print "Backward Backward "
  print "distance:",dist
  if dist<20 :
      print "Object on the way "
      bot.doMove(100,100)
      sleep(0.5)
      bot.doMove(100,-100)
      sleep(0.1)
      nCollisions=nCollisions + 1;
      #session.attributes["collisions"] = nCollisions
  bot.doMove(-100,-100)
  sleep(STEPS)

def checkforObstacle(direction):
  global bot
  print "BOTTTTTTT Here ...."
  print bot
  if bot == None:
        bot = initMBot();

  print "The direction I am going is %s " %(direction)
  try:
    if (direction == "forward"):
        print ">>>>>>>>>>>>>>>>> Now moving foward ....."
        bot.doMove(100,100)
        bot.requestUltrasonicSensor(1,3, onDistanceForward)
    else:
        print "<<<<<<<<<<<<< Now Moving backwards <<<<<<<<< "
        bot.doMove(-100,-100)
        bot.requestUltrasonicSensor(1,3, onDistanceBackward)
  except Exception,ex:
       print "Exception..... ..... "
       print str(ex)


@ask.launch
def new_game():
    global bot
    bot = initMBot();
    welcome_msg = render_template('robot')
    return question(welcome_msg)


def robot_stop():
    global bot
    print "BOTTTTTTT Here ...."
    print bot
    if bot == None:
          bot = initMBot();
    bot.doMove(0,0);

def robot_move(elapsed_time, direction):
    print "Running    : " + direction
    print "Time to run: %d " % elapsed_time
    t_forward = 0;
    while (t_forward<=elapsed_time):
        print "Moving forward for %d seconds " % t_forward
        checkforObstacle(direction)
        t_forward = t_forward + STEPS
    robot_stop();
    #collisions = session.attributes["collisions"]

@ask.intent("StopIntent")
def robot_stop_all():
        stop_msg   = render_template("stop")
        robot_stop();
        return question(stop_msg);

@ask.intent("CollisionIntent")
def avoid_collision():
     return True;

@ask.intent("ForwardIntent", convert={'elapsed_time': int})
def robot_move_forward(elapsed_time):
        global nCollisions
        print "running forward"
        e_time = elapsed_time
        robot_move(e_time, "forward")
        forward_msg   = render_template("forward_move",  elapsed_time = elapsed_time,   n_collisions=nCollisions)
        return question(forward_msg)

@ask.intent("BackwardIntent", convert={"elapsed_time": int } )
def robot_move_backward(elapsed_time):
        global nCollisions
        print "running backward"
        e_time = elapsed_time
        robot_move(e_time, "backward")
        backward_msg  = render_template("backward_move", elapsed_time = elapsed_time,   n_collisions=nCollisions)
        return question(backward_msg)

def robot_turn(elapsed_time, direction):
    global bot
    global STEPS
    print "Moving %s time elapsed = %d" % (direction, elapsed_time)
    t_turnning = 0;
    while (t_turnning <= elapsed_time ):
       print "Now muving .... %d ", t_turnning;
       t_turnning = t_turnning + STEPS
       if (direction == "right"):
          bot.doMove(100, 50)
       else:
          bot.doMove(50, 100)
       sleep(STEPS)

@ask.intent("TurnRightIntent", convert={'elapsed_time': int })
def moveright(elapsed_time):
    print "TUrning to the right for %d seconds "%elapsed_time
    turn_right_msg = render_template("turn_right", elapsed_time=elapsed_time)
    robot_turn(elapsed_time, "right")
    robot_stop()
    return question(turn_right_msg)

@ask.intent("TurnLeftIntent", convert={'elapsed_time' : int })
def moveleft(elapsed_time):
    print "Turning to the left for %d seconds "%elapsed_time
    robot_turn(elapsed_time, "left")
    robot_stop()
    turn_left_msg  = render_template("turn_left",  elapsed_time=elapsed_time)
    return question(turn_left_msg)

@ask.intent("FunIntent")
def fun_intent():
    #numbers = [randint(0, 9) for _ in range(3)]
    fun_msg = render_template('fun_msg')
    return question(fun_msg)

@ask.intent("YesIntent")
def next_round():
    #numbers = [randint(0, 9) for _ in range(3)]
    #round_msg = render_template('round', numbers=numbers)
    #session.attributes['numbers'] = numbers[::-1]  # reverse
    #return question(round_msg)
    instructions_msg = render_template("instructions")
    return question(instructions_msg)

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    winning_numbers = session.attributes['numbers']
    if [first, second, third] == winning_numbers:
        msg = render_template('win')
    else:
        msg = render_template('lose')
    return question(msg)

@ask.intent("HowManyChromecastsIntent")
def howmanycasts():
    casts = pychromecast.get_chromecasts()
    names = [str(c.device.friendly_name) for c in casts]
    numberofcast_msg = render_template('numberofcasts', n_casts=len(names), names=names);
    return statement(numberofcast_msg)

if __name__ == '__main__':
    print "Loading Robot Game Server / HTTP"
    #initMBot();
    app.run(debug=True, use_reloader=False)
    #g.bot.close()
