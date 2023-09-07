import random


class Species:
    def __init__(self, speed, size, hostility) -> None:
        self.speed = speed
        self.size = size
        self.hostility = hostility
        self.size_values = []
        self.speed_values = []
        self.food_values = []
        self.status_values = []
        self.lastgenpower = []
        self.allavgs = []

    def create_speed(self):
        new_speed = round(random.normalvariate(self.speed, 8))
        if new_speed <= 0:
            new_speed = 1
        self.speed_values.append(new_speed)
        self.food_values.append(10)
        self.status_values.append(True)
        return new_speed

    def create_size(self):
        new_size = round(random.normalvariate(self.size, 8))
        if new_size <= 0:
            new_size = 1
        self.size_values.append(new_size)
        return new_size

    def get_creature_values(self, index):
        if 0 <= index < len(self.speed_values):
            return (
                self.speed_values[index],
                self.size_values[index],
                self.food_values[index],
                self.hostility,
                (self.speed_values[index] + self.size_values[index]
                 * self.food_values[index]),
                self.status_values[index]
            )
        else:
            return None, None, None, None, None, False

    def calculate_meeting_probability(self, creature_index1, creature_index2):
        speed_difference = abs(
            self.speed_values[creature_index1] - self.speed_values[creature_index2])
        size_difference = abs(
            self.size_values[creature_index1] - self.size_values[creature_index2])
        food_difference = abs(
            self.food_values[creature_index1] - self.food_values[creature_index2])
        # Adjust the meeting probability calculation for less frequent meetings
        meeting_probability = 1.0 / \
            (1.0 + speed_difference + size_difference + food_difference + 50)
        return meeting_probability

    def meet_or_not(self, creature_index1, creature_index2):
        meeting_probability = self.calculate_meeting_probability(
            creature_index1, creature_index2)

        return random.random() < meeting_probability

    def create_offspring(self, psize, pspeed):
        new_speed = round(random.normalvariate(pspeed, pspeed/2))
        if new_speed <= 0:
            new_speed = 1
        new_size = round(random.normalvariate(psize, psize/2))
        if new_size <= 0:
            new_size = 1
        self.size_values.append(new_size)
        self.speed_values.append(new_speed)
        self.food_values.append(10)
        self.status_values.append(True)
        self.lastgenpower.append((new_speed+new_size)*10)
        if len(self.lastgenpower) == 25:
            a = 0
            for i in self.lastgenpower:
                a += i
            self.allavgs.append(a/len(self.lastgenpower))
            self.lastgenpower.clear()


# remove hostility and put in a food amount factor

print('try to keep the numbers between 1 and 100 and keep the two species traits simalear otherwise one will go extinct quickly')
speed = int(input('speed trait(species 1): '))
size = int(input('size trait(species 1): '))
hostility = 'P'
speed2 = int(input('speed trait(species 2): '))
size2 = int(input('size trait(species 2): '))
hostility2 = 'A'
s1 = Species(speed, size, hostility)
s2 = Species(speed2, size2, hostility2)
for i in range(50):
    s1.create_speed()
    s1.create_size()
    s2.create_speed()
    s2.create_size()

s2poweravg = []
s1poweravg = []

# get average of each to compare to at the end
for i in range(len(s2.status_values)):
    creature_speed2, creature_size2, creature_food2, creature_hostility2, power2, status2 = s2.get_creature_values(
        i)
    s2poweravg.append(power2)
for i in range(len(s1.status_values)):
    creature_speed, creature_size, creature_food, creature_hostility, power, status = s1.get_creature_values(
        i)
    s1poweravg.append(power)

h = 0
for i in s1poweravg:
    h += i
gen1s1avg = h/len(s1poweravg)

t = 0
for i in s2poweravg:
    t += i
gen1s2avg = t/len(s2poweravg)

s1.allavgs.append(gen1s1avg)
s2.allavgs.append(gen1s2avg)

duration = int(input('Number of years to run(above 100 recommended): '))

# begin simulation


def fight(index, outcome):
    creature_speed, creature_size, creature_food, creature_hostility, power, status = s1.get_creature_values(
        index)
    creature_speed2, creature_size2, creature_food2, creature_hostility2, power2, status2 = s2.get_creature_values(
        index)
    if outcome == 'fight':
        # check which creature has a higher power
        powerdif = powerdiff(power, power2)
        if power > power2:
            rand = random.normalvariate(100, powerdif)
            rand2 = random.normalvariate(100, powerdif*1.5)
        elif power2 > power:
            rand = random.normalvariate(100, powerdif*1.5)
            rand2 = random.normalvariate(100, powerdif)
        else:
            rand = random.normalvariate(100, powerdif)
            rand2 = random.normalvariate(100, powerdif)
        if abs(rand-100) > abs(rand2-100):
            return 'c1kill'
        elif abs(rand-100) < abs(rand2-100):
            return 'c2kill'
        else:
            return random.choice(['c1kill', 'c2kill'])
    else:
        speed_diff = abs(creature_speed - creature_speed2)
        food_diff = abs(creature_food - creature_food2)
        if power > power2:
            # creature 2 is running away
            prob = speed_diff + food_diff
            prob2 = speed_diff + food_diff
            if creature_speed2 > creature_speed:
                prob += speed_diff
            else:
                prob2 += speed_diff
            # if creature 2 has a higher speed or food use it for the prob if it has less use it against
            if creature_food2 > creature_food:
                prob += food_diff
            else:
                prob2 += food_diff
            rand = random.normalvariate(100, prob)
            rand2 = random.normalvariate(100, prob2)
            if abs(rand-100) > abs(rand2-100):
                return 'c1kill'
            elif abs(rand-100) < abs(rand2-100):
                return 'c2escape'
            else:
                return random.choice(['c1kill', 'c2escape'])
        else:
            # creature 1 is running away
            prob = speed_diff + food_diff
            prob2 = speed_diff + food_diff
            if creature_speed2 > creature_speed:
                prob += speed_diff
            else:
                prob2 += speed_diff
            # if creature 2 has a higher speed or food use it for the prob if it has less use it against
            if creature_food2 > creature_food:
                prob += food_diff
            else:
                prob2 += food_diff
            rand = random.normalvariate(100, prob)
            rand2 = random.normalvariate(100, prob2)
            if abs(rand-100) > abs(rand2-100):
                return 'c1escape'
            elif abs(rand-100) < abs(rand2-100):
                return 'c2kill'
            else:
                return random.choice(['c1escape', 'c2kill'])
    # Determine the outcome of a fight based on their levels/powers
    # You can use random.randint() to simulate a fight outcome
    # Return the winning creature or None if they both escape


def powerdiff(power1, power2):
    return abs(power1-power2)


# make a total food in the enviorment and if it runs out then animals need to wait
#
#
#
# make the user pick how many of each species there are

with open('log.txt', 'w') as file:
    file.write("")

for year in range(duration):
    with open('log.txt', 'a') as file:
        file.write(f"-----Year {year}-----\n")
        file.write('\n')

    if year == 150:
        print('')

    for y in range(len(s1.food_values)):
        s1.food_values[y] -= .05
        if random.random() >= .4:
            s1.food_values[y] + 4

    for y in range(len(s2.food_values)):
        s2.food_values[y] -= .05
        if random.random() >= .4:
            s2.food_values[y] + 4

    # Update food values and remove creatures with status_value set to False
    for x in s2.food_values:
        if x <= 0:
            del s2.status_values[s2.food_values.index(x)]
            del s2.speed_values[s2.food_values.index(x)]
            del s2.size_values[s2.food_values.index(x)]
            del s2.food_values[s2.food_values.index(x)]
    for x in s1.food_values:
        if x <= 0:
            del s1.status_values[s1.food_values.index(x)]
            del s1.speed_values[s1.food_values.index(x)]
            del s1.size_values[s1.food_values.index(x)]
            del s1.food_values[s1.food_values.index(x)]
    # Update size and speed based on the previous year's values (growth or decay)
    # Simulate encounters
    if len(s1.speed_values) > len(s2.speed_values):
        for i in range(len(s2.speed_values)):
            # check if both creatures alive before making them meet
            for j in range(i + 1, len(s1.speed_values)):
                if s1.meet_or_not(i, j):
                    # Determine what happens when creatures meet (fight, escape, etc.)
                    creature_speed, creature_size, creature_food, creature_hostility, power, status = s1.get_creature_values(
                        i)
                    creature_speed2, creature_size2, creature_food2, creature_hostility2, power2, status2 = s2.get_creature_values(
                        i)
                    if powerdiff(power, power2) >= 200:
                        # determine which creature runs away
                        if power > power2:
                            outcome = 'c2run'
                        else:
                            outcome = 'c1run'
                    else:
                        outcome = 'fight'
                    fightoutcome = fight(i, outcome)
                    with open('log.txt', 'a') as file:
                        file.write(f"Creatures #{i} Encounter\n")
                        file.write(f'States Before Encounter\n')
                        file.write(
                            f'species 1 -- speed: {creature_speed}, size: {creature_size}, food: {creature_food}, level: {power}, alive: {status}\n')
                        file.write(
                            f'species 2 -- speed: {creature_speed2}, size: {creature_size2}, food: {creature_food2}, level: {power2}, alive: {status2}\n')
                        file.write(
                            f'What happens in encounter: {outcome}, {fightoutcome}, Stats After Fight\n')
                    if fightoutcome == 'c1kill':
                        s2.status_values[i] = False
                        s1.food_values[i] += 4.5
                    if fightoutcome == 'c2kill':
                        s1.status_values[i] = False
                        s2.food_values[i] += 4.5
                    if fightoutcome == 'c1escape':
                        s1.food_values[i] -= 2
                        s2.food_values[i] -= 2
                    if fightoutcome == 'c2escape':
                        s1.food_values[i] -= 2
                        s2.food_values[i] -= 2
                    if s2.food_values[i] == 0:
                        s2.status_values[i] = False
                    if s1.food_values[i] == 0:
                        s1.status_values[i] = False
                    with open('log.txt', 'a') as file:
                        file.write(
                            f'species 1 -- speed: {s1.speed_values[i]}, size: {s1.size_values[i]}, food: {s1.food_values[i]}, level: {(s1.speed_values[i] + s1.size_values[i]) * s1.food_values[i]}, alive: {s1.status_values[i]}\n')
                        file.write(
                            f'species 2 -- speed: {s2.speed_values[i]}, size: {s2.size_values[i]}, food: {s2.food_values[i]}, level: {(s2.speed_values[i] + s2.size_values[i]) * s2.food_values[i]}, alive: {s2.status_values[i]}\n')
                        file.write('\n')
                    break
    else:
        for i in range(len(s2.speed_values)):
            # check if both creatures alive before making them meet
            for j in range(i + 1, len(s1.speed_values)):
                if s1.meet_or_not(i, j):
                    # Determine what happens when creatures meet (fight, escape, etc.)
                    creature_speed, creature_size, creature_food, creature_hostility, power, status = s1.get_creature_values(
                        i)
                    creature_speed2, creature_size2, creature_food2, creature_hostility2, power2, status2 = s2.get_creature_values(
                        i)
                    if powerdiff(power, power2) >= 200:
                        # determine which creature runs away
                        if power > power2:
                            outcome = 'c2run'
                        else:
                            outcome = 'c1run'
                    else:
                        outcome = 'fight'
                    fightoutcome = fight(i, outcome)
                    with open('log.txt', 'a') as file:
                        file.write(f"Creatures #{i} Encounter\n")
                        file.write(f'States Before Encounter\n')
                        file.write(
                            f'species 1 -- speed: {creature_speed}, size: {creature_size}, food: {creature_food}, level: {power}, alive: {status}\n')
                        file.write(
                            f'species 2 -- speed: {creature_speed2}, size: {creature_size2}, food: {creature_food2}, level: {power2}, alive: {status2}\n')
                        file.write(
                            f'What happens in encounter: {outcome}, {fightoutcome}, Stats After Fight\n')
                    if fightoutcome == 'c1kill':
                        s2.status_values[i] = False
                        s1.food_values[i] += 4.5
                    if fightoutcome == 'c2kill':
                        s1.status_values[i] = False
                        s2.food_values[i] += 4.5
                    if fightoutcome == 'c1escape':
                        s1.food_values[i] -= 2
                        s2.food_values[i] -= 2
                    if fightoutcome == 'c2escape':
                        s1.food_values[i] -= 2
                        s2.food_values[i] -= 2
                    if s2.food_values[i] == 0:
                        s2.status_values[i] = False
                    if s1.food_values[i] == 0:
                        s1.status_values[i] = False
                    with open('log.txt', 'a') as file:
                        file.write(
                            f'species 1 -- speed: {s1.speed_values[i]}, size: {s1.size_values[i]}, food: {s1.food_values[i]}, level: {(s1.speed_values[i] + s1.size_values[i]) * s1.food_values[i]}, alive: {s1.status_values[i]}\n')
                        file.write(
                            f'species 2 -- speed: {s2.speed_values[i]}, size: {s2.size_values[i]}, food: {s2.food_values[i]}, level: {(s2.speed_values[i] + s2.size_values[i]) * s2.food_values[i]}, alive: {s2.status_values[i]}\n')
                        file.write('\n')
                    break
    # Check for reproduction
    if year % 20 == 0:
        for i in range(len(s1.speed_values)):
            if s1.status_values[i] == True:
                if s1.food_values[i] >= 5:
                    # If food >= 5, reproduce with a chance
                    if random.random() >= 0.6:
                        # Create an offspring and add its attributes to lists
                        if year < duration - 25:
                            s1.create_offspring(
                                s1.size_values[i], s1.speed_values[i])
        for i in range(len(s2.speed_values)):
            if s2.status_values[i] == True:
                if s2.food_values[i] >= 5:
                    # If food >= 5, reproduce with a chance
                    if random.random() >= 0.6:
                        # Create an offspring and add its attributes to lists
                        if year < duration - 25:
                            s2.create_offspring(
                                s2.size_values[i], s2.speed_values[i])
                        # get average power of last gen

# Print the final results after the simulation


print('')
print('Power Averages')
if len(s1.allavgs) > len(s2.allavgs):
    for i in range(len(s1.allavgs)):
        print(f'Generation {i}')
        try:
            print(
                f'Species 1: {s1.allavgs[i]}, Species 2: {s2.allavgs[i]}')
        except:
            print(
                f'Species 1: {s1.allavgs[i]}, Species 2: Extinct')
        print('')
else:
    for i in range(len(s2.allavgs)):
        print(f'Generation {i}')
        try:
            print(
                f'Species 1: {s1.allavgs[i]}, Species 2: {s2.allavgs[i]}')
        except:
            print(
                f'Species 1: Extinct, Species 2: {s2.allavgs[i]}')
        print('')

print('Summary')
print(f'Species 1: Generation 0 power average: {s1.allavgs[0]} Last generation power average: {s1.allavgs[-1]} Peak power average: {max(s1.allavgs)}. {round(((max(s1.allavgs) - s1.allavgs[0]) / s1.allavgs[0]) * 100)}% {"increase" if max(s1.allavgs) >= s1.allavgs[0] else "decrease"}')
print(f'Species 2: Generation 0 power average: {s2.allavgs[0]} Last generation power average: {s2.allavgs[-1]} Peak power average: {max(s2.allavgs)}. {round(((max(s2.allavgs) - s2.allavgs[0]) / s2.allavgs[0]) * 100)}% {"increase" if max(s2.allavgs) >= s2.allavgs[0] else "decrease"}')


# let user examine the results
l = 0
l2 = 0
for i in s1.status_values:
    if i == True:
        l += 1
for i in s2.status_values:
    if i == True:
        l2 += 1
print('')
print(f'species 1 remaining: {l}, species 2 remaining: {l2}')
print('')
end = input('press any key to exit')
