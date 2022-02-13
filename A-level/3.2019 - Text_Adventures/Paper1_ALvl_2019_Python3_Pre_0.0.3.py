#Skeleton Program code for the AQA A Level Paper 1 Summer 2019 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.5.1 programming environment

import random
import pickle
import os
import struct

INVENTORY = 1001
MINIMUM_ID_FOR_ITEM = 2001
ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS = 10000

class Place():
  def __init__(self):
    self.Description = ""
    self.ID = self.North = self.East = self.South = self.West = self.Up = self.Down = 0

class Character():
  def __init__(self):
    self.Name = self.Description = ""
    self.ID = self.CurrentLocation = 0

class Item():
  def __init__(self):
    self.ID = self.Location = 0
    self.Description = self.Status = self.Name = self.Commands = self.Results = ""

def GetInstruction():
  print(os.linesep)
  Instruction = input("> ").lower()
  return Instruction

def ExtractCommand(Instruction):
  Command = ""
  if " " not in Instruction:
    return Instruction, Instruction
  while len(Instruction) > 0 and Instruction[0] != " ":
    Command += Instruction[0]
    Instruction = Instruction[1:]
  while len(Instruction) > 0 and Instruction[0] == " ":
    Instruction = Instruction[1:]
  return Command, Instruction

def Go(You, Direction, CurrentPlace):
  Moved = True
  print("Currentplace is ",You.CurrentLocation-1)
  print("Place ",CurrentPlace.North,CurrentPlace.East,CurrentPlace.South,CurrentPlace.West,CurrentPlace.Up,CurrentPlace.Down)
  if Direction == "north":
    if CurrentPlace.North == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.North
  elif Direction == "east":
    if CurrentPlace.East == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.East
  elif Direction == "south":
    if CurrentPlace.South == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.South
  elif Direction == "west":
    if CurrentPlace.West == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.West
  elif Direction == "up":
    if CurrentPlace.Up == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.Up
  elif Direction == "down":
    if CurrentPlace.Down == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.Down
  else:
    Moved = False
  if not Moved:
    print("You are not able to go in that direction.")
  print("Currentplace is now ",You.CurrentLocation-1)
  return You, Moved

def DisplayDoorStatus(Status):
  if Status == "open":
    print("The door is open.")
  else:
    print("The door is closed.")

def DisplayContentsOfContainerItem(Items, ContainerID):
  print("It contains: ", end = "")
  ContainsItem = False
  for Thing in Items:
    if Thing.Location == ContainerID:
      if ContainsItem:
        print(", ", end = "")
      ContainsItem = True
      print(Thing.Name, end = "")
  if ContainsItem:
    print(".")
  else:
    print("nothing.")

def Examine(Items, Characters, ItemToExamine, CurrentLocation):
  Count = 0
  if ItemToExamine == "inventory":
    DisplayInventory(Items)
  else:
    IndexOfItem = GetIndexOfItem(ItemToExamine, -1, Items)
    if IndexOfItem != -1:
      if Items[IndexOfItem].Location == INVENTORY or Items[IndexOfItem].Location == CurrentLocation:
        print(Items[IndexOfItem].Description)
        if "door" in Items[IndexOfItem].Name:
          DisplayDoorStatus(Items[IndexOfItem].Status)
        if "container" in Items[IndexOfItem].Status:
          DisplayContentsOfContainerItem(Items, Items[IndexOfItem].ID)
        return
    while Count < len(Characters):
      if Characters[Count].Name == ItemToExamine and Characters[Count].CurrentLocation == CurrentLocation:
        print(Characters[Count].Description)
        return
      Count += 1
    print("You cannot find " + ItemToExamine + " to look at.")

def GetPositionOfCommand(CommandList, Command):
  # Find position of the input command in the command list
  Position = Count = 0
  while Count <= len(CommandList) - len(Command):
    # There are enough letters left in the command list for this command to be there
    if CommandList[Count:Count + len(Command)] == Command:
      # This is the required command
      return Position
    elif CommandList[Count] == ",":
      # Found a comma, so the command is later in the list
      Position += 1
    # Move to the next character
    Count += 1
  return Position

def GetResultForCommand(Results, Position):
  # Find the result for the input position
  # Results are separated by semi-colons
  Count = 0
  CurrentPosition = 0
  ResultForCommand = ""
  while CurrentPosition < Position and Count < len(Results):
    # Not yet reached the required result
    if Results[Count] == ";":
      # Next result
      CurrentPosition += 1
    Count += 1
  while Count < len(Results):
    # Add all the characters that make up the result
    if Results[Count] == ";":
      # Text terminates at the semi-colon
      break
    ResultForCommand += Results[Count]
    Count += 1
  return ResultForCommand

def Say(Speech):
  print()
  print(Speech)
  print()

def ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand):
  # Extract the first two components for this result
  # e.g   "say,It is attached to the wall"
  # produces Subcommand="say" and subcommandparameter="It is attached to the wall"
  # Note that the outputs are appended to in this routine.
  Count = 0
  while Count < len(ResultForCommand) and ResultForCommand[Count] != ",":
    # Not yet reached the comma or the end of this result
    SubCommand += ResultForCommand[Count]
    Count += 1
  # Remainder of result are parameters - read until end of result or until a comma or semi-colon is reached
  Count += 1
  while Count < len(ResultForCommand):
    if ResultForCommand[Count] != "," and ResultForCommand[Count] != ";":
      # Not a comma or a semi-colon - add to string
      SubCommandParameter += ResultForCommand[Count]
    else:
      # found a comma or semi-colon - terminate
      break
    Count += 1
  return SubCommand, SubCommandParameter

def ChangeLocationReference(Direction, NewLocationReference, Places, IndexOfCurrentLocation, Opposite):
  # Next line is DEAD CODE that wastes memory
  ThisPlace = Place()
  ThisPlace = Places[IndexOfCurrentLocation]
  # It is better to have brackets in the following conditions as the "and" must be
  # applied before the "or"
  if (Direction == "north" and not Opposite) or (Direction == "south" and Opposite):
    # Direction is north or the opposite of south
    ThisPlace.North = NewLocationReference
  elif Direction == "east" and not Opposite or Direction == "west" and Opposite:
    ThisPlace.East = NewLocationReference
  elif Direction == "south" and not Opposite or Direction == "north" and Opposite:
    ThisPlace.South = NewLocationReference
  elif Direction == "west" and not Opposite or Direction == "east" and Opposite:
    ThisPlace.West = NewLocationReference
  elif Direction == "up" and not Opposite or Direction == "down" and Opposite:
    ThisPlace.Up = NewLocationReference
  elif Direction == "down" and not Opposite or Direction == "up" and Opposite:
    ThisPlace.Down = NewLocationReference
  # Next line is pointless as this is already the case (as they already point to the same place)
  Places[IndexOfCurrentLocation] = ThisPlace
  return Places

def OpenClose(Open, Items, Places, ItemToOpenClose, CurrentLocation):
  # Open or close a door
  Count = 0
  Direction = ""
  DirectionChange = ""
  ActionWorked = False
  if Open:
    Command = "open"
  else:
    Command = "close"
  while Count < len(Items) and not ActionWorked:
    if Items[Count].Name == ItemToOpenClose:
      # This a an item of the type to be opened/closed
      if Items[Count].Location == CurrentLocation:
        # Item is in the current location
        if len(Items[Count].Commands) >= 4:
          # Command consists of at least 4 items
          if Command in Items[Count].Commands:
            # The item be opened or closed
            if Items[Count].Status == Command:
              # Already in the state requested
              return -2, Items, Places
            elif Items[Count].Status == "locked":
              # Item is locked and so cant be changed
              return -3, Items, Places
            # Locate the command in the command list
            Position = GetPositionOfCommand(Items[Count].Commands, Command)
            # Find the result for the command in this position
            ResultForCommand = GetResultForCommand(Items[Count].Results, Position)
            # Extract the first two components of the result
            Direction, DirectionChange = ExtractResultForCommand(Direction, DirectionChange, ResultForCommand)
            # Open or close the door
            Items = ChangeStatusOfItem(Items, Count, Command)
            Count2 = 0
            ActionWorked = True
            while Count2 < len(Places):
              if Places[Count2].ID == int(CurrentLocation):
                Places = ChangeLocationReference(Direction, int(DirectionChange), Places, Count2, False)
              elif Places[Count2].ID == int(DirectionChange):
                Places = ChangeLocationReference(Direction, CurrentLocation, Places, Count2, True)
              Count2 += 1
            if Items[Count].ID > ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS:
              IndexOfOtherSideOfDoor = GetIndexOfItem("", Items[Count].ID - ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS, Items)
            else:
              IndexOfOtherSideOfDoor = GetIndexOfItem("", Items[Count].ID + ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS, Items)
            Items = ChangeStatusOfItem(Items, IndexOfOtherSideOfDoor, Command)
            Count = len(Items) + 1            
    Count += 1
  if not ActionWorked:
    return -1, Items, Places
  return int(DirectionChange), Items, Places

def GetIndexOfItem(ItemNameToGet, ItemIDToGet, Items):
  Count = 0
  StopLoop = False
  while not StopLoop and Count < len(Items):
    if (ItemIDToGet == -1 and Items[Count].Name == ItemNameToGet) or Items[Count].ID == ItemIDToGet:
      StopLoop = True
    else:
      Count += 1
  if not StopLoop:
    return -1
  else:
    return Count

def ChangeLocationOfItem(Items, IndexOfItem, NewLocation):
  # Change the location of the item
  # The next line is DEAD CODE and creates memory for an object that is then never used
  ThisItem = Item()
  ThisItem = Items[IndexOfItem]
  ThisItem.Location = NewLocation
  # The next line is pointless as this is already true
  Items[IndexOfItem] = ThisItem
  return Items

def ChangeStatusOfItem(Items, IndexOfItem, NewStatus):
  # Change the status of the item
  # eg. a door can become "open" or "close"
  # The next line is DEAD CODE and creates memory for an object that is then never used
  ThisItem = Item()
  ThisItem = Items[IndexOfItem]
  ThisItem.Status = NewStatus
  # The next line is pointless as this is already true
  Items[IndexOfItem] = ThisItem
  return Items

def GetRandomNumber(LowerLimitValue, UpperLimitValue):
  return random.randint(LowerLimitValue, UpperLimitValue)
      
def RollDie(Lower, Upper): 
  LowerLimitValue = 0
  if Lower.isnumeric():
    LowerLimitValue = int(Lower)
  else:
    while LowerLimitValue < 1 or LowerLimitValue > 6:
      LowerLimitValue = int(input("Enter minimum: "))
  UpperLimitValue = 0
  if Upper.isnumeric():
    UpperLimitValue = int(Upper)
  else:
    while UpperLimitValue < LowerLimitValue or UpperLimitValue > 6:
      UpperLimitValue = int(input("Enter maximum: "))
  return GetRandomNumber(LowerLimitValue, UpperLimitValue)

def ChangeStatusOfDoor(Items, CurrentLocation, IndexOfItemToLockUnlock, IndexOfOtherSideItemToLockUnlock):
  if CurrentLocation == Items[IndexOfItemToLockUnlock].Location or CurrentLocation == Items[IndexOfOtherSideItemToLockUnlock].Location:
    if Items[IndexOfItemToLockUnlock].Status == "locked":
      Items = ChangeStatusOfItem(Items, IndexOfItemToLockUnlock, "close")
      Items = ChangeStatusOfItem(Items, IndexOfOtherSideItemToLockUnlock, "close")
      Say(Items[IndexOfItemToLockUnlock].Name + " now unlocked.")
    elif Items[IndexOfItemToLockUnlock].Status == "close":
      Items = ChangeStatusOfItem(Items, IndexOfItemToLockUnlock, "locked")
      Items = ChangeStatusOfItem(Items, IndexOfOtherSideItemToLockUnlock, "locked")
      Say(Items[IndexOfItemToLockUnlock].Name + " now locked.")
    else:
      Say(Items[IndexOfItemToLockUnlock].Name + " is open so can't be locked.")
  else:
    Say("Can't use that key in this location.")
  return Items

def UseItem(Items, ItemToUse, CurrentLocation, Places):
  StopGame = False
  SubCommand = ""
  SubCommandParameter = ""
  IndexOfItem = GetIndexOfItem(ItemToUse, -1, Items)
  if IndexOfItem != -1:
    if Items[IndexOfItem].Location == INVENTORY or (Items[IndexOfItem].Location == CurrentLocation and "usable" in Items[IndexOfItem].Status):
      Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "use")
      ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
      SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
      if SubCommand == "say":
        Say(SubCommandParameter)
      elif SubCommand == "lockunlock":
        IndexOfItemToLockUnlock = GetIndexOfItem("", int(SubCommandParameter), Items)
        IndexOfOtherSideItemToLockUnlock = GetIndexOfItem("", int(SubCommandParameter) + ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS, Items)
        Items = ChangeStatusOfDoor(Items, CurrentLocation, IndexOfItemToLockUnlock, IndexOfOtherSideItemToLockUnlock)
      elif SubCommand == "roll":
        Say("You have rolled a " + str(RollDie(ResultForCommand[5], ResultForCommand[7])))
      return StopGame, Items
  print("You can't use that!")
  return StopGame, Items

def ReadItem(Items, ItemToRead, CurrentLocation):
  SubCommand = ""
  SubCommandParameter = ""
  IndexOfItem = GetIndexOfItem(ItemToRead, -1, Items)
  if IndexOfItem == -1:
    print("You can't find " + ItemToRead + ".")
  elif not "read" in Items[IndexOfItem].Commands:
    print("You can't read " + ItemToRead + ".")
  elif Items[IndexOfItem].Location != CurrentLocation and Items[IndexOfItem].Location != INVENTORY:
    print("You can't find " + ItemToRead + ".")
  else:
    Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "read")
    ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
    SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
    if SubCommand == "say":
      Say(SubCommandParameter)

def HoldingLarge(Items):
  # Check Inventory for any large items
  found=False
  for Thing in Items:
    if Thing.Location == INVENTORY and "large" in Thing.Status:
      found=True
  return found
      
def GetItem(Items, ItemToGet, CurrentLocation):
  # Pick up an item if possible
  SubCommand = ""
  SubCommandParameter = ""
  CanGet = False
  IndexOfItem = GetIndexOfItem(ItemToGet, -1, Items)
  if IndexOfItem == -1:
    print("You can't find " + ItemToGet + ".")
  elif Items[IndexOfItem].Location == INVENTORY:
    print("You have already got that!")
  elif not "get" in Items[IndexOfItem].Commands:
    print("You can't get " + ItemToGet + ".")
  elif Items[IndexOfItem].Location >= MINIMUM_ID_FOR_ITEM and Items[GetIndexOfItem("", Items[IndexOfItem].Location, Items)].Location != CurrentLocation:
    print("You can't find " + ItemToGet + ".")
  elif Items[IndexOfItem].Location < MINIMUM_ID_FOR_ITEM and Items[IndexOfItem].Location != CurrentLocation:
    print("You can't find " + ItemToGet + ".")
  elif ("large" in Items[IndexOfItem].Status) and HoldingLarge(Items):
    # Already holding a large item - cannot carry another
    print("You are already carrying a large item so you can't get "+ItemToGet+".")
  else:
    CanGet = True
  if CanGet:
    Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "get")
    ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
    SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
    if SubCommand == "say":
      Say(SubCommandParameter)
    elif SubCommand == "win":
      Say("You have won the game")
      return True, Items
    if "gettable" in Items[IndexOfItem].Status:
      Items = ChangeLocationOfItem(Items, IndexOfItem, INVENTORY)
      print("You have got that now.")
  return False, Items

def CheckIfDiceGamePossible(Items, Characters, OtherCharacterName):
  PlayerHasDie = False
  PlayersInSameRoom = False
  IndexOfPlayerDie = -1
  IndexOfOtherCharacter = -1
  IndexOfOtherCharacterDie = -1
  OtherCharacterHasDie = False
  for Thing in Items:
    if Thing.Location == INVENTORY and "die" in Thing.Name:
      PlayerHasDie = True
      IndexOfPlayerDie = GetIndexOfItem("", Thing.ID, Items)
  Count = 1
  while Count < len(Characters) and not PlayersInSameRoom:
    if Characters[0].CurrentLocation == Characters[Count].CurrentLocation and Characters[Count].Name == OtherCharacterName:
      PlayersInSameRoom = True
      for Thing in Items:
        if Thing.Location == Characters[Count].ID and "die" in Thing.Name:
          OtherCharacterHasDie = True
          IndexOfOtherCharacterDie = GetIndexOfItem("", Thing.ID, Items)
          IndexOfOtherCharacter = Count
    Count += 1
  return PlayerHasDie and PlayersInSameRoom and OtherCharacterHasDie, IndexOfPlayerDie, IndexOfOtherCharacter, IndexOfOtherCharacterDie

def TakeItemFromOtherCharacter(Items, OtherCharacterID):
  ListOfIndicesOfItemsInInventory = []
  ListOfNamesOfItemsInInventory = []
  Count = 0
  while Count < len(Items):
    if Items[Count].Location == OtherCharacterID:
      ListOfIndicesOfItemsInInventory.append(Count)
      ListOfNamesOfItemsInInventory.append(Items[Count].Name)
    Count += 1
  Count = 1
  print("Which item do you want to take?  They have:", end = "")
  print(ListOfNamesOfItemsInInventory[0], end = "")
  while Count < len(ListOfNamesOfItemsInInventory) - 1:
    print(",", ListOfNamesOfItemsInInventory[Count], end = "")
    Count += 1
  print(".")
  ChosenItem = input()
  if ChosenItem in ListOfNamesOfItemsInInventory:
    print("You have that now.")
    Pos = ListOfNamesOfItemsInInventory.index(ChosenItem)
    Items = ChangeLocationOfItem(Items, ListOfIndicesOfItemsInInventory[Pos], INVENTORY)
  else:
    print("They don't have that item, so you don't take anything this time.")
  return Items

def TakeRandomItemFromPlayer(Items, OtherCharacterID):
  ListOfIndicesOfItemsInInventory = []
  Count = 0
  while Count < len(Items):
    if Items[Count].Location == INVENTORY:
      ListOfIndicesOfItemsInInventory.append(Count)
    Count += 1
  rno = GetRandomNumber(0, len(ListOfIndicesOfItemsInInventory) - 1)
  print("They have taken your " + Items[ListOfIndicesOfItemsInInventory[rno]].Name + ".")
  Items = ChangeLocationOfItem(Items, ListOfIndicesOfItemsInInventory[rno], OtherCharacterID)
  return Items

def PlayDiceGame(Characters, Items, OtherCharacterName):
  PlayerScore = 0
  OtherCharacterScore = 0
  DiceGamePossible, IndexOfPlayerDie, IndexOfOtherCharacter, IndexOfOtherCharacterDie = CheckIfDiceGamePossible(Items, Characters, OtherCharacterName)
  if not DiceGamePossible:
    print("You can't play a dice game.")
  else:
    Position = GetPositionOfCommand(Items[IndexOfPlayerDie].Commands, "use")
    ResultForCommand = GetResultForCommand(Items[IndexOfPlayerDie].Results, Position)
    PlayerScore = RollDie(ResultForCommand[5], ResultForCommand[7])
    print("You rolled a " + str(PlayerScore) + ".")
    Position = GetPositionOfCommand(Items[IndexOfOtherCharacterDie].Commands, "use")
    ResultForCommand = GetResultForCommand(Items[IndexOfOtherCharacterDie].Results, Position)
    OtherCharacterScore = RollDie(ResultForCommand[5], ResultForCommand[7])
    print("They rolled a " + str(OtherCharacterScore) + ".")
    if PlayerScore > OtherCharacterScore:
      print("You win!")
      Items = TakeItemFromOtherCharacter(Items, Characters[IndexOfOtherCharacter].ID)
    elif PlayerScore < OtherCharacterScore:
      print("You lose!")
      Items = TakeRandomItemFromPlayer(Items, Characters[IndexOfOtherCharacter].ID)
    else:
      print("Draw!")
  return Items
      
def MoveItem(Items, ItemToMove, CurrentLocation):
  SubCommand = ""
  SubCommandParameter = ""
  IndexOfItem = GetIndexOfItem(ItemToMove, -1, Items)
  if IndexOfItem != -1:
    if Items[IndexOfItem].Location == CurrentLocation:
      if len(Items[IndexOfItem].Commands) >= 4:
        if "move" in Items[IndexOfItem].Commands:
          Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "move")
          ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
          SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
          if SubCommand == "say":
            Say(SubCommandParameter)
          else:
            print("You can't move " + ItemToMove + ".")
        else:
          print("You can't move " + ItemToMove + ".")
      return
  print("You can't find " + ItemToMove + ".")

def DisplayInventory(Items):
  print()
  print("You are currently carrying the following items:")
  for Thing in Items:
    if Thing.Location == INVENTORY:
      print(Thing.Name)
    
def DisplayGettableItemsInLocation(Items, CurrentLocation):
  ContainsGettableItems = False
  ListOfItems = "On the floor there is: "
  for Thing in Items:
    if Thing.Location == CurrentLocation and "gettable" in Thing.Status:
      if ContainsGettableItems:
        ListOfItems += ", "
      ListOfItems += Thing.Name
      ContainsGettableItems = True
  if ContainsGettableItems:
    print(ListOfItems + ".")
    
def DisplayOpenCloseMessage(ResultOfOpenClose, OpenCommand):
  if ResultOfOpenClose >= 0:
    if OpenCommand:
      Say("You have opened it.")
    else:
      Say("You have closed it.")
  elif ResultOfOpenClose == -3:
    Say("You can't do that, it is locked.")
  elif ResultOfOpenClose == -2:
    Say("It already is.")
  elif ResultOfOpenClose == -1:
    Say("You can't open that.")
       
def PlayGame(Characters, Items, Places):
  StopGame = False
  Moved = True
  while not StopGame:
    if Moved:
      print()
      print()
      print(Places[Characters[0].CurrentLocation - 1].Description)
      DisplayGettableItemsInLocation(Items, Characters[0].CurrentLocation)
      Moved = False
    Instruction = GetInstruction()
    Command, Instruction = ExtractCommand(Instruction)
    if Command == "get":
      # pick up an item
      StopGame, Items = GetItem(Items, Instruction, Characters[0].CurrentLocation)
    elif Command == "use":
      # use an item
      StopGame, Items = UseItem(Items, Instruction, Characters[0].CurrentLocation, Places)
    elif Command == "go":
      # move your character to another room
      Characters[0], Moved = Go(Characters[0], Instruction, Places[Characters[0].CurrentLocation - 1])
    elif Command == "read":
      # ????
      ReadItem(Items, Instruction, Characters[0].CurrentLocation)
    elif Command == "examine":
      # See what you are currently carrying or ???
      Examine(Items, Characters, Instruction, Characters[0].CurrentLocation)
    elif Command == "open":
      # Open an item (door etc.)
      ResultOfOpenClose, Items, Places = OpenClose(True, Items, Places, Instruction, Characters[0].CurrentLocation)
      DisplayOpenCloseMessage(ResultOfOpenClose, True)
    elif Command == "close":
      # Close an item (door etc.)
      ResultOfOpenClose, Items, Places = OpenClose(False, Items, Places, Instruction, Characters[0].CurrentLocation)
      DisplayOpenCloseMessage(ResultOfOpenClose, False)
    elif Command == "move":
      # Move an item
      MoveItem(Items, Instruction, Characters[0].CurrentLocation)
    elif Command == "say":
      # Output the phrase in this command
      Say(Instruction)
    elif Command == "playdice":
      # Roll the dice as a challenge to another character?
      Items = PlayDiceGame(Characters, Items, Instruction)
    elif Command == "quit":
      Say("You decide to give up, try again another time.")
      StopGame = True
    else:
      print("Sorry, you don't know how to " + Command + ".")
  input()

def LoadGame(Filename, Characters, Items, Places):
  try:
    # Open the binary file
    f = open(Filename, "rb")
    NoOfCharacters = pickle.load(f)
    for Count in range(NoOfCharacters):
      TempCharacter = Character()
      TempCharacter.ID = pickle.load(f)
      TempCharacter.Name = pickle.load(f)
      TempCharacter.Description = pickle.load(f)
      TempCharacter.CurrentLocation = pickle.load(f)
      Characters.append(TempCharacter)
    print("Current Location is ",Characters[0].CurrentLocation-1)
    print("Room  N E W S U D")
    NoOfPlaces = pickle.load(f)
    for Count in range(0, NoOfPlaces):
      TempPlace = Place()
      TempPlace.ID = pickle.load(f)
      TempPlace.Description = pickle.load(f)
      TempPlace.North = pickle.load(f)
      TempPlace.East = pickle.load(f)
      TempPlace.South = pickle.load(f)
      TempPlace.West = pickle.load(f)
      TempPlace.Up = pickle.load(f)
      TempPlace.Down = pickle.load(f)
      print(Count,"   ",TempPlace.North,TempPlace.East,TempPlace.South,TempPlace.West,TempPlace.Up,TempPlace.Down)
      Places.append(TempPlace)
    NoOfItems = pickle.load(f)
    for Count in range(0, NoOfItems):
      TempItem = Item()
      TempItem.ID = pickle.load(f)
      TempItem.Description = pickle.load(f)
      TempItem.Status = pickle.load(f)
      TempItem.Location = pickle.load(f)
      TempItem.Name = pickle.load(f)
      TempItem.Commands = pickle.load(f)
      TempItem.Results = pickle.load(f)
      Items.append(TempItem)
    print("Item ID's")
    print("===========================================================")
    for Count in range(0, NoOfItems):
      print("Items : ",Count,Items[Count].ID)
    print("Item Descriptionss")
    print("===========================================================")
    for Count in range(0, NoOfItems):
      print("Items : ",Count,Items[Count].Description)
    print("Item Status")
    print("===========================================================")
    for Count in range(0, NoOfItems):
      print("Items : ",Count,Items[Count].Status)
    print("Item Location")
    print("===========================================================")
    for Count in range(0, NoOfItems):
      print("Items : ",Count,Items[Count].Location)
    print("Item Name")
    print("===========================================================")
    for Count in range(0, NoOfItems):
      print("Items : ",Count,Items[Count].Name)
    print("Item Commands")
    print("===========================================================")
    for Count in range(0, NoOfItems):
      print("Items : ",Count,Items[Count].Commands)
    print("Item Results")
    for Count in range(0, NoOfItems):
      print("Items : ",Count,Items[Count].Results)

    for Count in range(0, NoOfItems):
      print("Item ",Count,Items[Count].Name.rjust(15)," Statuses: ", Items[Count].Status.rjust(40)," Commands: ",Items[Count].Commands)
    return True, Characters, Items, Places
  except:
    return False, Characters, Items, Places

def Main():
  Items = []
  Characters = []
  Places = []
  Filename = input("Enter filename> ") + ".gme"
  print()
  GameLoaded, Characters, Items, Places = LoadGame(Filename, Characters, Items, Places)
  if GameLoaded:
    PlayGame(Characters, Items, Places)
  else:
    print("Unable to load game.")
    input()

if __name__ == "__main__":
  Main()
