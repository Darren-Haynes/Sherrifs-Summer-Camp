import csv
import random
from collections import OrderedDict

import activities


class SummerCamp:
    def __init__(self) -> None:
        self.main_data = self.instantiate_data()
        self.land = activities.land
        self.water = activities.water
        self.assigned_land_activity = {k: v[0] for k, v in self.main_data.items()}
        self.assigned_water_9am_activity = {}
        self.assigned_water_10am_activity = {}
        self.land_1st_choice_totals = self.assigned_activity_totals(
            self.land, self.assigned_land_activity
        )
        self.water_9am_1st_choice_totals = {}
        self.water_10am_1st_choice_totals = {}
        self.land_below_min, self.land_no_votes = self.calc_land_below_min()
        self.water_9am_below_min = {}
        self.water_9am_no_votes = {}
        self.water_10am_below_min = {}
        self.water_10am_no_votes = {}
        self.land_above_max = self.calc_land_above_max()
        self.water_9am_above_max = {}
        self.water_10am_above_max = {}
        self.land_inbetween = self.filter_elems_inbetween(
            self.land,
            self.land_below_min,
            self.land_above_max,
            self.land_no_votes,
            self.land_1st_choice_totals,
        )
        self.water_9am_inbetween = {}
        self.water_10am_inbetween = {}
        self.land_9am = activities.nineAM_land
        self.land_10am = activities.tenAM_land
        self.water_9am = activities.nineAM_water
        self.water_10am = activities.tenAM_water
        self.land_9am_count = 0
        self.land_10am_count = 0
        self.water_9am_count = 0
        self.water_10am_count = 0
        self.kids_9am = []
        self.kids_10am = []

    def instantiate_data(self):
        """
        Turn raw data from an excel sheet file into the format:
        {kids_name = [land_choice1, land_choice2, land_choice3,
                        water_choice1, water_choice2, water_choice3]}
        Each kid chooses their 3 prefered land activity choices and their 3
        prefered water activities.
        """
        data = {}
        with open("TestData/rand-data-118-kids.txt", "r") as file:
            # with open("TestData/keegans-data.txt", "r") as file:
            lines = file.readlines()
            random.shuffle(lines)
            for line in lines:
                sep = line.strip().split("\t")
                name = " ".join(sep[0:2])
                activities = []
                for activity in sep[3:]:
                    activities.append(activity.lower())
                data[name] = activities
        return data

    def instantiate_data_txt(self):
        """
        Turn raw data from a text file into the format:
        {kids_name = [land_choice1, land_choice2, land_choice3,
                      water_choice1, water_choice2, water_choice3]}
        Each kid chooses their 3 prefered land activity choices and their 3
        prefered water activities.
        """
        data = {}
        # with open("TestData/rand-data-100-kids.txt", "r") as file:
        with open("TestData/rand-data-118-kids.txt", "r") as file:
            # with open("TestData/rand-data-118-archery.txt", "r") as file:
            # with open("TestData/rand-data2.txt", "r") as file:  # 100 people
            # with open("TestData/rand-data3.txt", "r") as file:  # 50 people
            # with open("Data/orig-data.txt", "r") as file:
            lines = file.readlines()
            random.shuffle(lines)
            for line in lines:
                sep = line.strip().split(",")
                data[sep[0]] = sep[1:]
        print(data)
        return data

    def instantiate_water(self):
        self.all_9am_and_10am_kids()
        for kid in self.kids_9am:
            choice = self.main_data[kid][3]
            self.assigned_water_9am_activity[kid] = choice
        for kid in self.kids_10am:
            choice = self.main_data[kid][3]
            self.assigned_water_10am_activity[kid] = choice
        return

    def calc_element_min(self, element):
        """
        Find the activity that can accomadate the least amount of kids.
        """
        count = -1
        for values in element.values():
            if count == -1:
                count = values[0]
            if values[0] < count:
                count = values[0]
        return count

    def calc_kids_min(self):
        """
        Find the least amount children the summer camp can accept by finding
        which activity in land and water that can accept the least # of kids.
        Then return the minimum of the 2.
        """
        land_min = self.calc_element_min(self.land)
        water_min = self.calc_element_min(self.water)
        return min(land_min, water_min)

    def calc_element_max(self, element):
        """
        Running total of the max amount of kids each activity can accomadate.
        """
        count = 0
        for values in element.values():
            count += values[1]
            if values[2] == 2:
                count += values[1]
        return count

    def calc_kids_max(self):
        """
        Find the most amount children the summer camp can accept by calculating
        the most amount of kids each activity in land and water can accommodate.
        Then return the greater of the 2.
        """
        land_max = self.calc_element_max(self.land)
        water_max = sum([m[1] if m != 2 else m[1] * 2 for m in self.water.values()])
        return max(land_max, water_max)

    def calc_water_below_min(self, choice_totals):
        """
        Returns dict:
        key: activity -- such as archery or fishing
        value: int of how many people the minimum allowed for that activity
        """
        below_min = []
        zero_votes = []
        for activity, total in choice_totals.items():
            minimum = self.water[activity][0]
            if total == 0:
                zero_votes.append([activity, total - minimum])
                continue
            if total < minimum:
                below_min.append([activity, total - minimum])
        below_min.sort(key=lambda x: x[1])
        zero_votes.sort(key=lambda x: x[1], reverse=True)

        below_dict = OrderedDict({k: v for (k, v) in below_min})
        zero_dict = OrderedDict({k: v for (k, v) in zero_votes})
        return below_dict, zero_dict

    def calc_land_below_min(self):
        """
        Returns dict:
        key: activity -- such as archery or fishing
        value: int of how many people the minimum allowed for that activity
        """
        below_min = []
        zero_votes = []
        for activity, total in self.land_1st_choice_totals.items():
            minimum = self.land[activity][0]
            if total == 0:
                zero_votes.append([activity, total - minimum])
                continue
            if self.land[activity][2] == 2:
                minimum *= 2
            if total < minimum:
                below_min.append([activity, total - minimum])
        below_min.sort(key=lambda x: x[1])
        zero_votes.sort(key=lambda x: x[1], reverse=True)

        below_dict = OrderedDict({k: v for (k, v) in below_min})
        zero_dict = OrderedDict({k: v for (k, v) in zero_votes})
        return below_dict, zero_dict

    def calc_water_above_max(self, choice_totals):
        above_max = []
        for activity, total in choice_totals.items():
            maximum = self.water[activity][1]
            if total > maximum:
                above_max.append([activity, total - maximum])
        above_max.sort(key=lambda x: x[1], reverse=True)
        above_dict = OrderedDict({k: v for (k, v) in above_max})
        return above_dict

    def calc_land_above_max(self):
        """
        Returns dict:
        key: activity -- such as archery or fishing
        value: int of how many people exceed the max allowed for that activity
        """
        above_max = []
        for activity, total in self.land_1st_choice_totals.items():
            maximum = self.land[activity][1]
            if self.land[activity][2] == 2:
                maximum *= 2
            if total > maximum:
                above_max.append([activity, total - maximum])
        above_max.sort(key=lambda x: x[1], reverse=True)
        above_dict = OrderedDict({k: v for (k, v) in above_max})
        return above_dict

    def count_assigned_activity(self, activity, elem_assigned):
        """
        Return how many kids for a specific time-slot (land or water at 9am or
        10am are the time-slots) are assigned to a specific activity.
        """
        count = 0
        for choice in elem_assigned.values():
            if choice == activity:
                count += 1
        return count

    def filter_activities(self, activities, elem):
        """
        Since we will be taking people from these activities to boost the
        activities that are below min threshold, then we don't want to take from
        activities that are just at the minimum. And also we want to start with
        those closest to or are at max threshold.
        """
        filtered = []
        for activity, below_max in activities.items():
            if elem[activity][0] == below_max:
                continue
            else:
                filtered.append(activity)
        return filtered

    def filter_elems_inbetween(
        self, elem, elem_below, elem_above, elem_no_votes, elem_choice_totals
    ):
        """
        Inbetween meaning the activities children have chosen that are
        >= to the min amount of kids allowed for that activity and <= the max
        amount of kids. Thus we return the activities that have enough kids,
        and filter out those activities that don't have enough kids or too many.
        """
        inbetween = {}
        for activity in elem.keys():
            if (
                activity not in elem_below
                and activity not in elem_above
                and activity not in elem_no_votes
            ):
                shortfall = elem[activity][1] - elem_choice_totals[activity]
                if shortfall == 0:
                    continue
                if shortfall < 0:
                    shortfall = elem[activity][1] * 2 - elem_choice_totals[activity]

                inbetween[activity] = shortfall
        return inbetween

    def filter_sort_land_inbetween(self, elem, elem_inbetween):
        """
        Returns a list of all the names that are above minumim and below or
        equal to max of each activity, in sort by order of activites that have
        the most people to spare.
        """
        spare = []
        for activity in elem_inbetween.keys():
            names = self.get_names_by_activity(activity, elem_inbetween)
            minimum = elem[activity][0]
            actual = len(names)
            if len(names) > minimum * 2:
                minimum *= 2
            available = actual - minimum
            if available > 0:
                max_names = random.sample(names, available)
                spare.append((max_names, available))

        spare.sort(key=lambda x: x[1], reverse=True)

        spares = []
        for s in spare:
            for name in s[0]:
                spares.append(name)
        return spares

    def update_choice_in_land_below_min(
        self,
        name,
        choice,
        main_activity,
        elem_below,
        elem_above,
        elem_assigned,
        elem_totals,
    ):
        elem_below[choice] += 1
        elem_assigned[name] = choice
        elem_totals[choice] += 1
        elem_totals[main_activity] -= 1
        elem_above[main_activity] -= 1

        if elem_below[choice] == 0:
            del elem_below[choice]

        if elem_above[main_activity] == 0:
            del elem_above[main_activity]
            return True
        return False

    def update_choice_in_land_below_min_and_below_max(
        self, name, choice, main_activity, elem_assigned, elem_totals, elem_above
    ):
        elem_assigned[name] = choice
        elem_totals[choice] += 1
        elem_totals[main_activity] -= 1
        elem_above[main_activity] -= 1
        if elem_above[main_activity] == 0:
            del elem_above[main_activity]
            return True
        return False

    def update_matching_inbetween_below_min(
        self,
        choices,
        main_activity,
        elem,
        elem_assigned,
        elem_totals,
        elem_below,
        elem_inbetween,
    ):
        for choice, name in choices:
            count = self.count_assigned_activity(choice, elem_assigned)
            if count <= elem[choice][0]:
                continue
            if choice in elem_inbetween:
                elem_assigned[name] = main_activity
                elem_totals[choice] -= 1
                elem_totals[main_activity] += 1
                elem_below[main_activity] += 1
                elem_inbetween[choice] -= 1
                if elem_below[main_activity] == 0:
                    del elem_below[main_activity]
                    elem_inbetween[main_activity] = elem[main_activity][0]
                    return True
        return False

    def update_matching_inbetween(
        self,
        choices,
        main_activity,
        elem_inbetween,
        elem_assigned,
        elem_totals,
        elem_above,
        elem,
    ):
        for name, choice in choices:
            if self.count_assigned_activity(
                choice, elem_assigned
            ) >= self.get_activity_max(choice, elem, elem_assigned):
                continue
            if choice in elem_inbetween:
                elem_assigned[name] = choice
                elem_totals[choice] += 1
                elem_totals[main_activity] -= 1
                elem_above[main_activity] -= 1
                elem_inbetween[choice] -= 1
                if elem_inbetween[choice] == 0:
                    del elem_inbetween[choice]
                if elem_above[main_activity] == 0:
                    del elem_above[main_activity]
                    return True
        return False

    def update_matching_exactly_min(
        self,
        choices,
        main_activity,
        elem_inbetween,
        elem_assigned,
        elem_totals,
        elem_above,
        elem,
    ):
        for name, choice in choices:
            if self.count_assigned_activity(
                choice, elem_assigned
            ) >= self.get_activity_max(choice, elem, elem_assigned):
                continue
            if choice in elem_inbetween:
                elem_assigned[name] = choice
                elem_totals[choice] += 1
                elem_totals[main_activity] -= 1
                elem_above[main_activity] -= 1
                elem_inbetween[choice] -= 1
                if elem_inbetween[choice] == 0:
                    del elem_inbetween[choice]
                if elem_above[main_activity] == 0:
                    del elem_above[main_activity]
                    return True
        return False

    def update_matching_below_min(
        self,
        choices,
        main_activity,
        elem_below,
        elem_above,
        elem_assigned,
        elem_totals,
        elem,
    ):
        for name, choice in choices:
            if choice in elem_below:
                if self.update_choice_in_land_below_min(
                    name,
                    choice,
                    main_activity,
                    elem_below,
                    elem_above,
                    elem_assigned,
                    elem_totals,
                ):
                    return True

            elif elem_totals[choice] < elem[choice][1]:
                if self.update_choice_in_land_below_min_and_below_max(
                    name, choice, main_activity, elem_assigned, elem_totals, elem_above
                ):
                    return True
        return False

    def get_activity_max(self, activity, elem, elem_assigned):
        """
        Note that if the activity is in 2 time slots, thus 9am and 10am and also
        there are enough people assigned to the activity to fulfill the minimum
        occupancy requirements for 2 times slots then the returned max is get_2nd_3rd_choices_in_between
        to be double.
        """
        act_max = elem[activity][1]
        act_min = elem[activity][0] * 2
        act_count = self.count_assigned_activity(activity, elem_assigned)
        if elem[activity][2] == 2 and act_count > act_min:
            act_max *= 2
        return act_max

    def get_2nd_3rd_and_no_choices(
        self, main_activity, elem_below, elem_assigned, elem, not_chosen=False
    ):
        activities_below = elem_below.keys()
        choice2 = []
        choice3 = []
        no_choice = []
        land_2nd_choice = 1 if elem == self.land else 4
        land_3rd_choice = 2 if elem == self.land else 5
        for name, choice1 in elem_assigned.items():
            if choice1 == main_activity:
                if self.main_data[name][land_2nd_choice] in activities_below:
                    choice2.append([name, self.main_data[name][land_2nd_choice]])
                elif self.main_data[name][land_3rd_choice] in activities_below:
                    choice3.append([name, self.main_data[name][land_3rd_choice]])
                else:
                    no_choice.append(name)

        if not_chosen:
            return no_choice
        return choice2, choice3

    def get_names_by_activity(self, activity, elem_assigned):
        names = []
        for name, sport in elem_assigned.items():
            if sport == activity:
                names.append(name)
        return names

    def get_2nd_3rd_choices_in_between(
        self, main_activity, activities, elem, elem_assigned
    ):
        """
        Find people who have a specific activity as their 2nd and 3rd choice,
        starting with activities that are maxed out and closest to maxed out first.
        """
        activity_list = self.filter_activities(activities, elem)
        choice_num2 = 1 if elem == self.land else 4
        choice_num3 = 2 if elem == self.land else 5
        choice2 = []
        choice3 = []
        for activity in activity_list:
            names = self.get_names_by_activity(activity, elem_assigned)
            for name in names:
                if self.main_data[name][choice_num2] == main_activity:
                    choice2.append([activity, name])
                if self.main_data[name][choice_num3] == main_activity:
                    choice3.append([activity, name])
        random.shuffle(choice2)
        random.shuffle(choice3)
        return choice2, choice3

    def above_max_to_not_maxed_out(
        self,
        main_activity,
        elem_inbetween,
        elem_assigned,
        elem_totals,
        elem_above,
        elem,
    ):
        choice2, choice3 = self.get_2nd_3rd_and_no_choices(
            main_activity, elem_inbetween, elem_assigned, elem
        )
        if self.update_matching_inbetween(
            choice2,
            main_activity,
            elem_inbetween,
            elem_assigned,
            elem_totals,
            elem_above,
            elem,
        ):
            return True

        if self.update_matching_inbetween(
            choice3,
            main_activity,
            elem_assigned,
            elem_inbetween,
            elem_totals,
            elem_above,
            elem,
        ):
            return True

        return False

    def below_min_to_not_maxed_out_no_match(
        self,
        main_activity,
        elem,
        elem_assigned,
        elem_totals,
        elem_below,
        elem_inbetween,
    ):
        """
        This differs to function 'below_min_to_not_maxed_out' in that it doesn't
        care about a persons 2nd or 3rd choice. If this function is running it's
        because we have already exhausted 2nd and 3rd choice options. Now we
        give some poor kid an activity they didn't ask for :(
        """
        names = self.filter_sort_land_inbetween(elem, elem_inbetween)
        for name in names:
            count = self.count_assigned_activity(main_activity, elem_assigned)
            if count == elem[main_activity][0]:
                break
            curr_activity = elem_assigned[name]
            elem_assigned[name] = main_activity
            elem_totals[curr_activity] -= 1
            elem_totals[main_activity] += 1
            elem_below[main_activity] += 1
            elem_inbetween[curr_activity] -= 1
            if elem_below[main_activity] == 0:
                del elem_below[main_activity]
                elem_inbetween[main_activity] = elem[main_activity][0]
                return True
        return False

    def below_min_to_not_maxed_out(
        self,
        main_activity,
        elem_below,
        elem_assigned,
        elem_inbetween,
        elem,
        elem_totals,
    ):
        """
        For activities below the minimum threshold find a person we can
        move from another activity to this one. The other acivity will be above
        the min threshold and below the max threshold and thus have people to
        spare. This function first attempts to assign a person to their 1st
        choice, then 2nd choice; failing that it assigns a person to an activity
        they have not requested.
        """
        choice2, choice3 = self.get_2nd_3rd_choices_in_between(
            main_activity, elem_inbetween, elem, elem_assigned
        )

        if self.update_matching_inbetween_below_min(
            choice2,
            main_activity,
            elem,
            elem_assigned,
            elem_totals,
            elem_below,
            elem_inbetween,
        ):
            return True

        if self.update_matching_inbetween_below_min(
            choice3,
            main_activity,
            elem,
            elem_assigned,
            elem_totals,
            elem_below,
            elem_inbetween,
        ):
            return True

        if self.below_min_to_not_maxed_out_no_match(
            main_activity, elem, elem_assigned, elem_totals, elem_below, elem_inbetween
        ):
            print("WE REACHED HERE")
            print(main_activity)
            return True

        return False

    def above_to_below(
        self,
        main_activity,
        elem_below,
        elem_assigned,
        elem_inbetween,
        elem_totals,
        elem_above,
        elem,
    ):
        """
        For activities above the max threshold find a person we can
        move from this activity to one that is below the min threshold.
        This function honors a persons 2nd and 3rd choices.
        """
        choice2, choice3 = self.get_2nd_3rd_and_no_choices(
            main_activity, elem_below, elem_assigned, elem
        )

        if self.update_matching_below_min(
            choice2,
            main_activity,
            elem_below,
            elem_above,
            elem_assigned,
            elem_totals,
            elem,
        ):
            return True

        if self.update_matching_below_min(
            choice3,
            main_activity,
            elem_below,
            elem_above,
            elem_assigned,
            elem_totals,
            elem,
        ):
            return True

        if self.above_max_to_not_maxed_out(
            main_activity, elem_inbetween, elem_assigned, elem_totals, elem_above, elem
        ):
            return True
        return False

    def calc_above_and_below(self):
        """
        'below_min': total of activites short of minimum requirements.
        i.e if lacrosse is 2 people short and soccer 3 people short; total
        would be 5.
        'below_max': the upper limit of the below_min activities totalled.
        'above': total amount of activities in excess of the max people allowed.

        """
        # TODO: remove this method if it is not called.
        below_min = abs(sum(self.land_below_min.values()))
        below_max = below_min
        above = sum(self.land_above_max.values())
        for activity in self.land_below_min:
            below_max += self.land[activity][1] - self.land[activity][0]
        return below_min, below_max, above

    def within_bounds(self, activity, elem, elem_assigned):
        """
        Return True if the amount of kids assigned to an activity do not
        exceed the max allowed or fall below the min allowed.
        """
        act_min = elem[activity][0]
        act_max = elem[activity][1]
        act_count = self.count_assigned_activity(activity, elem_assigned)
        if elem == self.land:
            if elem[activity][2] == 2 and act_count > act_min * 2:
                act_max *= 2
                act_min *= 2
        return act_min <= act_count <= act_max

    def assigned_activity_totals(self, elem, assigned):
        """
        Return the total amount of kids assigned to each activity.
        Note that some activities have zero kids assigned and those activites
        will be ommitted.
        """
        totals = {}
        for activity in elem:
            totals[activity] = 0
        for data in assigned.values():
            totals[data] += 1
        return totals

    def update_above_max(
        self, name, choice, activity, elem, elem_assigned, elem_totals, elem_above
    ):
        if self.count_assigned_activity(choice, elem_assigned) == self.get_activity_max(
            choice, elem, elem_assigned
        ):
            return False
        elem_assigned[name] = choice
        elem_totals[choice] += 1
        elem_totals[activity] -= 1
        elem_above[activity] -= 1
        return True

    def assign_choices(
        self,
        activity,
        choice_num,
        act_count,
        elem,
        elem_assigned,
        elem_totals,
        elem_above,
        elem_below,
    ):
        names = self.get_names_by_activity(activity, elem_assigned)
        act_max = self.get_activity_max(activity, elem, elem_assigned)
        count = 0
        no_action = 0
        for name in names:
            print("Gimme a break")
            print(f"ACTIVITY: {activity}")
            if count == act_count - act_max:
                break

            if not self.within_bounds(activity, elem, elem_assigned):
                choice = self.main_data[name][choice_num]
                print(f"CHOICE WITHIN: {choice}")

                if self.count_assigned_activity(
                    choice, elem_assigned
                ) > self.get_activity_max(choice, elem, elem_assigned):
                    no_action += 1
                    print("I CANT GET NO ACTION")
                    continue
                else:
                    print("I am about to update")
                    self.update_above_max(
                        name,
                        choice,
                        activity,
                        elem,
                        elem_assigned,
                        elem_totals,
                        elem_above,
                    )
                    count += 1

            else:
                print("I should not be talking yet")
                print(name)
                print(activity)
                print(act_max)
                print(act_count)
                not_a_choice = self.get_2nd_3rd_and_no_choices(
                    activity,
                    elem_below,
                    elem_assigned,
                    elem,
                    not_chosen=True,
                )
                print("NOT A CHOICE")
                print(not_a_choice)
        return

    def assign_element(
        self, elem_above, elem_below, elem_inbetween, elem_assigned, elem, elem_totals
    ):
        """
        Main function that initiates the process of assigning kids to activities
        """
        count = 0
        # TODO: remove this count
        while elem_above or elem_below:
            # Case 1:
            # If at least one activity is overbooked and at least one is
            # overbooked then move kids from overbooked to underbooked
            # activities. Note this honors a kids 2nd and 3rd choice activities.
            # If these choices don't match the underbooked activites, then no
            # change is made.
            if elem_above and elem_below:
                for activity in list(elem_above.keys()):
                    self.above_to_below(
                        activity,
                        elem_below,
                        elem_assigned,
                        elem_inbetween,
                        elem_totals,
                        elem_above,
                        elem,
                    )

            # Case 2:
            # If at least one activity is overbooked and at least one is
            # overbooked then move kids from overbooked to underbooked
            # activities. Note this honors a kids 2nd and 3rd choice activities.
            # If these choices don't match the underbooked activites, then no
            # change is made.
            if elem_below:
                for activity in list(elem_below.keys()):
                    # TODO: follow this through.
                    self.below_min_to_not_maxed_out(
                        activity,
                        elem_below,
                        elem_assigned,
                        elem_inbetween,
                        elem,
                        elem_totals,
                    )

            if elem_above and elem_inbetween:
                for activity in list(elem_above.keys()):
                    self.above_max_to_not_maxed_out(
                        activity,
                        elem_inbetween,
                        elem_assigned,
                        elem_totals,
                        elem_above,
                        elem,
                    )
            #
            if elem_above:
                choice_num = 1 if elem == self.land else 4
                print(f"CHOICE NUM: {choice_num}")
                for activity in list(elem_above.keys()):
                    print("ELEM INBETWEEN 1")
                    print(elem_inbetween)
                    act_count = self.count_assigned_activity(activity, elem_assigned)
                    self.assign_choices(
                        activity,
                        choice_num,
                        act_count,
                        elem,
                        elem_assigned,
                        elem_totals,
                        elem_above,
                        elem_below,
                    )

            if elem_above:
                choice_num = 2 if elem == self.land else 5
                print(f"CHOICE NUM: {choice_num}")
                for activity in list(elem_above.keys()):
                    print("ELEM INBETWEEN 2")
                    print(elem_inbetween)
                    act_count = self.count_assigned_activity(activity, elem_assigned)
                    self.assign_choices(
                        activity,
                        choice_num,
                        act_count,
                        elem,
                        elem_assigned,
                        elem_totals,
                        elem_above,
                        elem_below,
                    )
            count += 1
            if count == 1:
                break
        return

    def assign_land(self):
        if self.error_checks():
            print("Program aborted.")
            return

        self.assign_element(
            self.land_above_max,
            self.land_below_min,
            self.land_inbetween,
            self.assigned_land_activity,
            self.land,
            self.land_1st_choice_totals,
        )
        self.assign_land_timeslots()
        return

    def assign_land_timeslots(self):
        both = {}
        not_both = {}
        for name, activity in self.assigned_land_activity.items():
            if activity in self.land_9am and activity in self.land_10am:
                if self.land_1st_choice_totals[activity] >= self.land[activity][0] * 2:
                    if activity in both:
                        if both[activity]:
                            both[activity] = False
                        else:
                            both[activity] = True
                    else:
                        both[activity] = True
                    if both[activity]:
                        self.land_9am[activity].append(name)
                        self.land_9am_count += 1
                    else:
                        self.land_10am[activity].append(name)
                        self.land_10am_count += 1

                else:
                    if activity in not_both:
                        not_both[activity].append(name)
                    else:
                        not_both[activity] = [name]

            elif activity in self.land_9am:
                self.land_9am[activity].append(name)
                self.land_9am_count += 1
            elif activity in self.land_10am:
                self.land_10am[activity].append(name)
                self.land_10am_count += 1

        if not_both:
            for activity, names in not_both.items():
                if self.land_9am_count >= self.land_10am_count:
                    self.land_10am[activity] = names
                    self.land_10am_count += len(names)
                else:
                    self.land_9am[activity] = names
                    self.land_9am_count += len(names)
        return

    def assign_water_timeslots(self, elem_assigned, elem_time, elem_count):
        for name, activity in elem_assigned.items():
            if activity in elem_time:
                elem_time[activity].append(name)
            else:
                elem_time[activity] = [name]
            elem_count += 1
        return

    def print_land(self, title_txt, elem, elem_time1, elem_time2, bounds=False):
        print(f"*** {title_txt} ***")
        names_count_9am = 0
        names_count_10am = 0
        for activity, names in elem_time1.items():
            if names:
                print(f"{activity.upper()}: {', '.join(names)}")
                if bounds:
                    min = elem[activity][0]
                    maxi = elem[activity][1]
                    oob = min <= len(names) <= maxi
                    print(f"{oob} ||  Min: {min} -- Max: {maxi}  Actual: {len(names)}")
                    names_count_9am += len(names)
        print("\n")
        print("*** 10AM LAND ACTIVITIES ***")
        for activity, names in elem_time2.items():
            if names:
                print(f"{activity.upper()}: {', '.join(names)}")
                if bounds:
                    min = elem[activity][0]
                    maxi = elem[activity][1]
                    oob = min <= len(names) <= maxi
                    print(f"{oob} ||  Min: {min} -- Max: {maxi}  Actual: {len(names)}")
                    names_count_10am += len(names)

        print(
            f"PRINT COUNT:  9am = {names_count_9am} -- 10am = {names_count_10am}",
            end="\n\n",
        )
        return

    def print_water(self, title_txt, elem, elem_time, bounds=False):
        print(f"*** {title_txt} ***")
        names_count_9am = 0
        for activity, names in elem_time.items():
            if names:
                print(f"{activity.upper()}: {', '.join(names)}")
                if bounds:
                    min = elem[activity][0]
                    maxi = elem[activity][1]
                    oob = min <= len(names) <= maxi
                    print(f"{oob} ||  Min: {min} -- Max: {maxi}  Actual: {len(names)}")
                    names_count_9am += len(names)
        print("\n")
        return names_count_9am

    def print_schedule(self, bounds=False):
        self.print_land(
            "9AM LAND ACTIVITIES",
            self.land,
            self.land_9am,
            self.land_10am,
            bounds=True,
        )

        names_count_9am = self.print_water(
            "9AM WATER ACTIVITIES",
            self.water,
            self.water_9am,
            bounds=True,
        )
        names_count_10am = self.print_water(
            "10AM WATER ACTIVITIES",
            self.water,
            self.water_10am,
            bounds=True,
        )
        print(f"PRINT COUNT:  9am = {names_count_9am} -- 10am = {names_count_10am}")
        return

    def all_9am_and_10am_kids(self):
        """
        Create lists of all the kids that have been assigned to 9am and 10am
        time slots.
        """
        for names in self.land_9am.values():
            self.kids_9am.extend(names)
        for names in self.land_10am.values():
            self.kids_10am.extend(names)
        return

    def assign_water_above_max(self):
        self.water_9am_above_max = self.calc_water_above_max(
            self.water_9am_1st_choice_totals
        )
        self.water_10am_above_max = self.calc_water_above_max(
            self.water_10am_1st_choice_totals
        )
        return

    def assign_water_totals(self):
        self.water_9am_1st_choice_totals = self.assigned_activity_totals(
            self.water, self.assigned_water_9am_activity
        )
        self.water_10am_1st_choice_totals = self.assigned_activity_totals(
            self.water, self.assigned_water_10am_activity
        )
        return

    def assign_water_below_min(self):
        self.water_9am_below_min, self.water_9am_no_votes = self.calc_water_below_min(
            self.water_9am_1st_choice_totals
        )
        self.water_10am_below_min, self.water_10am_no_votes = self.calc_water_below_min(
            self.water_10am_1st_choice_totals
        )
        return

    def assign_water_inbetween(self):
        self.water_9am_inbetween = self.filter_elems_inbetween(
            self.water,
            self.water_9am_below_min,
            self.water_9am_above_max,
            self.water_9am_no_votes,
            self.water_9am_1st_choice_totals,
        )
        self.water_10am_inbetween = self.filter_elems_inbetween(
            self.water,
            self.water_10am_below_min,
            self.water_10am_above_max,
            self.water_10am_no_votes,
            self.water_10am_1st_choice_totals,
        )
        return

    def assign_water(self):
        self.instantiate_water()
        self.assign_water_totals()
        self.assign_water_above_max()
        self.assign_water_below_min()
        self.assign_water_inbetween()

        self.assign_element(
            self.water_9am_above_max,
            self.water_9am_below_min,
            self.water_9am_inbetween,
            self.assigned_water_9am_activity,
            self.water,
            self.water_9am_1st_choice_totals,
        )
        self.assign_water_timeslots(
            self.assigned_water_9am_activity, self.water_9am, self.water_9am_count
        )

        self.assign_element(
            self.water_10am_above_max,
            self.water_10am_below_min,
            self.water_10am_inbetween,
            self.assigned_water_10am_activity,
            self.water,
            self.water_10am_1st_choice_totals,
        )

        self.assign_water_timeslots(
            self.assigned_water_10am_activity, self.water_10am, self.water_10am_count
        )

        return

    def output_to_csv(self):
        """
        Write all 4 time slots with the kids that are assigned to each activity.
        """
        with open("schedule.csv", "w", newline="") as csvfile:
            elements = [
                self.land_9am,
                self.land_10am,
                self.water_9am,
                self.water_10am,
            ]
            titles = [
                "9AM Land Activities",
                "10AM Land Activities",
                "9AM Water Activities",
                "10AM Water Activities",
            ]
            for elem, title in list(zip(elements, titles)):
                schedule_writer = csv.writer(
                    csvfile,
                    delimiter="\t",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )
                schedule_writer.writerow([title])
                for activity, names in elem.items():
                    schedule_writer.writerow([activity.upper()] + names)
                schedule_writer.writerow([])

    def error_too_many_kids(self):
        """If there are more kids than the total of the maximum of either the
        land of water activities than there are too many children for the camp.
        """
        count = self.calc_kids_max()
        if count < len(self.main_data):
            return (True, count)
        return (False, count)

    def error_not_enough_kids(self):
        """
        If there are less kids than the minumum kids allowed for the activity
        that requires less kids than all other activities; then there are not
        enough kids for the summer camp.
        Returning "True" means that are not enough kids.
        """
        count = self.calc_kids_min()
        if count > len(self.main_data):
            return (True, count)
        return (False, count)

    def error_checks(self):
        result = self.error_not_enough_kids()
        if result[0]:
            print(
                f"Not enough children to accomadate any single activity.\nOnly {result[1]} children imported from data"
            )
            return True

        result = self.error_too_many_kids()
        if result[0]:
            print(
                f"Too many children for the amount of activities provided.\nOnly {result[1]} children imported from data. \nAdd additional land and water sports or reduce number or children"
            )
            return True
