# coding = UTF-8

# 导入库
import numpy as np
import pandas as pd
from scipy.stats import uniform
from itertools import permutations

from application.academic.matchTheory.algorithm.class_BostonAlgorithm import StableMatcher as BostonStableMatcher
from application.academic.matchTheory.algorithm.class_BostonAlgorithm import Male as BostonStudent
from application.academic.matchTheory.algorithm.class_BostonAlgorithm import Female as BostonCollege
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import StableMatcher as DAAStableMatcher
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import Male as DAAStudent
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import Female as DAACollege

from application.academic.matchTheory.schoolChoice.sim_school_choice import SimSchoolChoice
from application.academic.matchTheory.schoolChoice.class_matchquality import MatchQuality

MODEL1 = False
MODEL2 = False
MODEL3 = True

if MODEL1:
    # 执行匹配次数
    times = 10
    # 学生数量
    student_number = 360

    total_college_numbers = []
    each_college_capacity = []
    mean_boston_matched_student_percent = []
    mean_boston_matched_percent_rank_1 = []
    mean_boston_matched_percent_rank_2 = []
    mean_boston_matched_percent_rank_3 = []
    mean_boston_matched_average_rank = []
    mean_da_matched_student_percent = []
    mean_da_matched_percent_rank_1 = []
    mean_da_matched_percent_rank_2 = []
    mean_da_matched_percent_rank_3 = []
    mean_da_matched_average_rank = []

    for college_number in range(2, 21, 2):
        print('round ', college_number)
        college_capacities = [int(student_number / college_number)] * college_number
        total_college_numbers.append(college_number)
        each_college_capacity.append(college_capacities)

        # 匹配过程
        boston_matched_student_percent = []
        boston_matched_percent_rank_1 = []
        boston_matched_percent_rank_2 = []
        boston_matched_percent_rank_3 = []
        boston_matched_average_rank = []
        da_matched_student_percent = []
        da_matched_percent_rank_1 = []
        da_matched_percent_rank_2 = []
        da_matched_percent_rank_3 = []
        da_matched_average_rank = []

        for t in range(times):
            print('time: ', t)
            sim = SimSchoolChoice(college_number=college_number,
                                  student_number=student_number,
                                  college_capacity=college_capacities)
            sim.generate_colleges_and_students()
            sim.generate_college_preference().generate_student_preference(sim.random_preferences)
            sim.generate_objects(College=BostonCollege, Student=BostonStudent)
            sim.matching(stable_matcher=BostonStableMatcher, echo=False)

            mq_boston = MatchQuality(colleges=sim.colleges, students=sim.students, matcher=sim.matcher)
            boston_matched_student_percent.append(mq_boston.matched_student_percent)
            boston_matched_percent_rank_1.append(mq_boston.matched_percent(rank=1))
            boston_matched_percent_rank_2.append(mq_boston.matched_percent(rank=2))
            boston_matched_percent_rank_3.append(mq_boston.matched_percent(rank=3))
            boston_matched_average_rank.append(mq_boston.matched_average_rank)

            sim.generate_objects(College=DAACollege, Student=DAAStudent)
            sim.matching(stable_matcher=DAAStableMatcher, echo=False)

            mq_da = MatchQuality(colleges=sim.colleges, students=sim.students, matcher=sim.matcher)
            da_matched_student_percent.append(mq_da.matched_student_percent)
            da_matched_percent_rank_1.append(mq_da.matched_percent(rank=1))
            da_matched_percent_rank_2.append(mq_da.matched_percent(rank=2))
            da_matched_percent_rank_3.append(mq_da.matched_percent(rank=3))
            da_matched_average_rank.append(mq_da.matched_average_rank)

        print("Boston: ", np.mean(boston_matched_student_percent))
        print("Boston Rank 1: ", np.mean(boston_matched_percent_rank_1))
        print("Boston Rank 2: ", np.mean(boston_matched_percent_rank_2))
        print("Boston Rank 3: ", np.mean(boston_matched_percent_rank_3))
        print("Boston average rank: ", np.mean(boston_matched_average_rank))
        mean_boston_matched_student_percent.append(np.mean(boston_matched_student_percent))
        mean_boston_matched_percent_rank_1.append(np.mean(boston_matched_percent_rank_1))
        mean_boston_matched_percent_rank_2.append(np.mean(boston_matched_percent_rank_2))
        mean_boston_matched_percent_rank_3.append(np.mean(boston_matched_percent_rank_3))
        mean_boston_matched_average_rank.append(np.mean(boston_matched_average_rank))

        print("DA: ", np.mean(da_matched_student_percent))
        print("DA Rank 1: ", np.mean(da_matched_percent_rank_1))
        print("DA Rank 2: ", np.mean(da_matched_percent_rank_2))
        print("DA Rank 3: ", np.mean(da_matched_percent_rank_3))
        print("DA average rank: ", np.mean(da_matched_average_rank))
        mean_da_matched_student_percent.append(np.mean(da_matched_student_percent))
        mean_da_matched_percent_rank_1.append(np.mean(da_matched_percent_rank_1))
        mean_da_matched_percent_rank_2.append(np.mean(da_matched_percent_rank_2))
        mean_da_matched_percent_rank_3.append(np.mean(da_matched_percent_rank_3))
        mean_da_matched_average_rank.append(np.mean(da_matched_average_rank))

    d = {'total_college_numbers':total_college_numbers,
         'each_college_capacity':each_college_capacity,
         'mean_boston_matched_student_percent':mean_boston_matched_student_percent,
         'mean_boston_matched_percent_rank_1':mean_boston_matched_percent_rank_1,
         'mean_boston_matched_percent_rank_2':mean_boston_matched_percent_rank_2,
         'mean_boston_matched_percent_rank_3':mean_boston_matched_percent_rank_3,
         'mean_boston_matched_average_rank':mean_boston_matched_average_rank,
         'mean_da_matched_student_percent':mean_da_matched_student_percent,
         'mean_da_matched_percent_rank_1':mean_da_matched_percent_rank_1,
         'mean_da_matched_percent_rank_2':mean_da_matched_percent_rank_2,
         'mean_da_matched_percent_rank_3':mean_da_matched_percent_rank_3,
         'mean_da_matched_average_rank':mean_da_matched_average_rank}

    result = pd.DataFrame(d)
    result.to_excel('result1.xlsx')

if MODEL2:
    # 执行匹配次数
    times = 20
    # 学生数量
    student_number = 300
    college_number = 2

    total_college_numbers = []
    each_college_capacity = []
    mean_da_matched_student_percent = []
    mean_da_matched_percent_rank_1 = []
    mean_da_matched_percent_rank_2 = []
    mean_da_matched_percent_rank_3 = []
    mean_da_matched_average_rank = []
    mean_da_matched_score_min = []
    mean_da_matched_score_mean = []
    mean_da_matched_score_std = []

    for college_quality in range(2, 9, 1):
        print('Starting...',college_quality)
        college_capacities = [int((student_number - 0) / college_number)] * college_number
        total_college_numbers.append(college_number)
        each_college_capacity.append(college_capacities)

        # 匹配过程
        da_matched_student_percent = []
        da_matched_percent_rank_1 = []
        da_matched_percent_rank_2 = []
        da_matched_percent_rank_3 = []
        da_matched_average_rank = []
        da_matched_score_min = []
        da_matched_score_mean = []
        da_matched_score_std = []

        for t in range(times):
            print('time: ', t)
            sim = SimSchoolChoice(college_number=college_number,
                                  student_number=student_number,
                                  college_capacity=college_capacities)
            sim.generate_colleges_and_students()
            sim.colleges_generator.set_academic([college_quality/10, 0.2])
            sim.generate_college_preference().generate_student_preference(sim.inclined_preferences_with_academic)
            sim.generate_objects(College=DAACollege, Student=DAAStudent)
            sim.matching(stable_matcher=DAAStableMatcher, echo=False)

            mq_da = MatchQuality(colleges=sim.colleges, students=sim.students, matcher=sim.matcher)
            da_matched_student_percent.append(mq_da.matched_student_percent)
            da_matched_percent_rank_1.append(mq_da.matched_percent(rank=1))
            da_matched_percent_rank_2.append(mq_da.matched_percent(rank=2))
            da_matched_average_rank.append(mq_da.matched_average_rank)
            da_matched_score_min.append(mq_da.score_summarize(fn=np.min))
            da_matched_score_mean.append(mq_da.score_summarize(fn=np.mean))
            da_matched_score_std.append(mq_da.score_summarize(fn=np.std))

        mean_da_matched_student_percent.append(np.mean(da_matched_student_percent))
        mean_da_matched_percent_rank_1.append(np.mean(da_matched_percent_rank_1))
        mean_da_matched_percent_rank_2.append(np.mean(da_matched_percent_rank_2))
        mean_da_matched_percent_rank_3.append(np.mean(da_matched_percent_rank_3))
        mean_da_matched_average_rank.append(np.mean(da_matched_average_rank))

        mean_da_matched_score_min.append(pd.DataFrame(da_matched_score_min).mean().to_dict())
        mean_da_matched_score_mean.append(pd.DataFrame(da_matched_score_mean).mean().to_dict())
        mean_da_matched_score_std.append(pd.DataFrame(da_matched_score_std).mean().to_dict())

    d1 = {'total_college_numbers':total_college_numbers,
         'each_college_capacity':each_college_capacity,
         'mean_da_matched_student_percent':mean_da_matched_student_percent,
         'mean_da_matched_percent_rank_1':mean_da_matched_percent_rank_1,
         'mean_da_matched_percent_rank_2':mean_da_matched_percent_rank_2,
         'mean_da_matched_average_rank':mean_da_matched_average_rank}

    d2 = pd.DataFrame(mean_da_matched_score_min)
    d2 = pd.concat([d2, pd.DataFrame(mean_da_matched_score_mean)], axis=1)
    d2 = pd.concat([d2, pd.DataFrame(mean_da_matched_score_std)], axis=1)

    result = pd.DataFrame(d1)
    result.to_excel('result2.xlsx')
    d2.to_excel('result2_d2.xlsx')

if MODEL3:
    # 执行匹配次数
    times = 20
    # 学生数量
    student_number = 300
    college_number = 2

    total_college_numbers = []
    each_college_capacity = []
    mean_da1_matched_student_percent = []
    mean_da1_matched_percent_rank_1 = []
    mean_da1_matched_percent_rank_2 = []
    mean_da1_matched_average_rank = []
    mean_da1_matched_score_min = []
    mean_da1_matched_score_mean = []
    mean_da1_matched_score_std = []

    mean_da2_matched_student_percent = []
    mean_da2_matched_percent_rank_1 = []
    mean_da2_matched_percent_rank_2 = []
    mean_da2_matched_average_rank = []
    mean_da2_matched_right_matched = []
    mean_da2_matched_under_matched = []
    mean_da2_matched_over_matched = []
    mean_da2_matched_score_min = []
    mean_da2_matched_score_mean = []
    mean_da2_matched_score_std = []

    mean_da3_matched_student_percent = []
    mean_da3_matched_percent_rank_1 = []
    mean_da3_matched_percent_rank_2 = []
    mean_da3_matched_average_rank = []
    mean_da3_matched_right_matched = []
    mean_da3_matched_under_matched = []
    mean_da3_matched_over_matched = []
    mean_da3_matched_score_min = []
    mean_da3_matched_score_mean = []
    mean_da3_matched_score_std = []

    for capacity_percent in range(1, 5, 1):
        print('Starting...',capacity_percent)
        college_capacities = [int(student_number * (1 - capacity_percent / 10)), int(student_number * capacity_percent / 10)]
        print(college_capacities)

        total_college_numbers.append(college_number)
        each_college_capacity.append(college_capacities)

        # 匹配过程
        da1_matched_student_percent = []
        da1_matched_percent_rank_1 = []
        da1_matched_percent_rank_2 = []
        da1_matched_average_rank = []
        da1_matched_score_min = []
        da1_matched_score_mean = []
        da1_matched_score_std = []

        # 匹配过程
        da2_matched_student_percent = []
        da2_matched_percent_rank_1 = []
        da2_matched_percent_rank_2 = []
        da2_matched_average_rank = []
        da2_matched_right_matched = []
        da2_matched_under_matched = []
        da2_matched_over_matched = []
        da2_matched_score_min = []
        da2_matched_score_mean = []
        da2_matched_score_std = []

        # 匹配过程
        da3_matched_student_percent = []
        da3_matched_percent_rank_1 = []
        da3_matched_percent_rank_2 = []
        da3_matched_average_rank = []
        da3_matched_right_matched = []
        da3_matched_under_matched = []
        da3_matched_over_matched = []
        da3_matched_score_min = []
        da3_matched_score_mean = []
        da3_matched_score_std = []

        for t in range(times):
            print('time: ', t)
            sim = SimSchoolChoice(college_number=college_number,
                                  student_number=student_number,
                                  college_capacity=[int(student_number/2), int(student_number/2)])
            sim.generate_colleges_and_students()
            sim.colleges_generator.set_academic([0.8, 0.2])
            sim.generate_college_preference().generate_student_preference(sim.inclined_preferences_with_academic)
            sim.generate_objects(College=DAACollege, Student=DAAStudent)
            sim.matching(stable_matcher=DAAStableMatcher, echo=False)

            sim2 = SimSchoolChoice(college_number=college_number,
                                  student_number=student_number,
                                  college_capacity=[int(student_number/2), int(student_number/2)],
                                  colleges=sim.colleges,
                                  students=sim.students)
            sim2.set_capacities(college_capacities)
            sim2.generate_objects(College=DAACollege, Student=DAAStudent)
            sim2.matching(DAAStableMatcher)

            sim3 = SimSchoolChoice(college_number=college_number,
                                   student_number=student_number,
                                   college_capacity=[int(student_number / 2), int(student_number / 2)],
                                   colleges=sim.colleges,
                                   students=sim.students)
            sim3.set_capacities(list(reversed(college_capacities)))
            sim3.generate_objects(College=DAACollege, Student=DAAStudent)
            sim3.matching(DAAStableMatcher)

            mq_da1 = MatchQuality(colleges=sim.colleges, students=sim.students, matcher=sim.matcher)
            da1_matched_student_percent.append(mq_da1.matched_student_percent)
            da1_matched_percent_rank_1.append(mq_da1.matched_percent(rank=1))
            da1_matched_percent_rank_2.append(mq_da1.matched_percent(rank=2))
            da1_matched_average_rank.append(mq_da1.matched_average_rank)
            da1_matched_score_min.append(mq_da1.score_summarize(fn=np.min))
            da1_matched_score_mean.append(mq_da1.score_summarize(fn=np.mean))
            da1_matched_score_std.append(mq_da1.score_summarize(fn=np.std))

            mq_da2 = MatchQuality(colleges=sim2.colleges, students=sim2.students, matcher=sim2.matcher)
            right_matched2, under_matched2, over_matched2 = mq_da2.mismatch(mq_da1)
            da2_matched_student_percent.append(mq_da2.matched_student_percent)
            da2_matched_percent_rank_1.append(mq_da2.matched_percent(rank=1))
            da2_matched_percent_rank_2.append(mq_da2.matched_percent(rank=2))
            da2_matched_average_rank.append(mq_da2.matched_average_rank)
            da2_matched_right_matched.append(right_matched2)
            da2_matched_under_matched.append(under_matched2)
            da2_matched_over_matched.append(over_matched2)
            da2_matched_score_min.append(mq_da2.score_summarize(fn=np.min))
            da2_matched_score_mean.append(mq_da2.score_summarize(fn=np.mean))
            da2_matched_score_std.append(mq_da2.score_summarize(fn=np.std))

            mq_da3 = MatchQuality(colleges=sim3.colleges, students=sim3.students, matcher=sim3.matcher)
            right_matched3, under_matched3, over_matched3 = mq_da3.mismatch(mq_da1)
            da3_matched_student_percent.append(mq_da3.matched_student_percent)
            da3_matched_percent_rank_1.append(mq_da3.matched_percent(rank=1))
            da3_matched_percent_rank_2.append(mq_da3.matched_percent(rank=2))
            da3_matched_average_rank.append(mq_da3.matched_average_rank)
            da3_matched_right_matched.append(right_matched3)
            da3_matched_under_matched.append(under_matched3)
            da3_matched_over_matched.append(over_matched3)
            da3_matched_score_min.append(mq_da3.score_summarize(fn=np.min))
            da3_matched_score_mean.append(mq_da3.score_summarize(fn=np.mean))
            da3_matched_score_std.append(mq_da3.score_summarize(fn=np.std))

        mean_da1_matched_student_percent.append(np.mean(da1_matched_student_percent))
        mean_da1_matched_percent_rank_1.append(np.mean(da1_matched_percent_rank_1))
        mean_da1_matched_percent_rank_2.append(np.mean(da1_matched_percent_rank_2))
        mean_da1_matched_average_rank.append(np.mean(da1_matched_average_rank))

        mean_da1_matched_score_min.append(pd.DataFrame(da1_matched_score_min).mean().to_dict())
        mean_da1_matched_score_mean.append(pd.DataFrame(da1_matched_score_mean).mean().to_dict())
        mean_da1_matched_score_std.append(pd.DataFrame(da1_matched_score_std).mean().to_dict())

        mean_da2_matched_student_percent.append(np.mean(da2_matched_student_percent))
        mean_da2_matched_percent_rank_1.append(np.mean(da2_matched_percent_rank_1))
        mean_da2_matched_percent_rank_2.append(np.mean(da2_matched_percent_rank_2))
        mean_da2_matched_average_rank.append(np.mean(da2_matched_average_rank))
        mean_da2_matched_right_matched.append(np.mean(da2_matched_right_matched))
        mean_da2_matched_under_matched.append(np.mean(da2_matched_under_matched))
        mean_da2_matched_over_matched.append(np.mean(da2_matched_over_matched))

        mean_da2_matched_score_min.append(pd.DataFrame(da2_matched_score_min).mean().to_dict())
        mean_da2_matched_score_mean.append(pd.DataFrame(da2_matched_score_mean).mean().to_dict())
        mean_da2_matched_score_std.append(pd.DataFrame(da2_matched_score_std).mean().to_dict())

        mean_da3_matched_student_percent.append(np.mean(da3_matched_student_percent))
        mean_da3_matched_percent_rank_1.append(np.mean(da3_matched_percent_rank_1))
        mean_da3_matched_percent_rank_2.append(np.mean(da3_matched_percent_rank_2))
        mean_da3_matched_average_rank.append(np.mean(da3_matched_average_rank))
        mean_da3_matched_right_matched.append(np.mean(da3_matched_right_matched))
        mean_da3_matched_under_matched.append(np.mean(da3_matched_under_matched))
        mean_da3_matched_over_matched.append(np.mean(da3_matched_over_matched))

        mean_da3_matched_score_min.append(pd.DataFrame(da3_matched_score_min).mean().to_dict())
        mean_da3_matched_score_mean.append(pd.DataFrame(da3_matched_score_mean).mean().to_dict())
        mean_da3_matched_score_std.append(pd.DataFrame(da3_matched_score_std).mean().to_dict())

    d1 = {'total_college_numbers':total_college_numbers,
         'each_college_capacity':each_college_capacity,
         'mean_da1_matched_student_percent':mean_da1_matched_student_percent,
         'mean_da1_matched_percent_rank_1':mean_da1_matched_percent_rank_1,
         'mean_da1_matched_percent_rank_2':mean_da1_matched_percent_rank_2,
         'mean_da1_matched_average_rank':mean_da1_matched_average_rank,
         'mean_da2_matched_student_percent': mean_da2_matched_student_percent,
         'mean_da2_matched_percent_rank_1': mean_da2_matched_percent_rank_1,
         'mean_da2_matched_percent_rank_2': mean_da2_matched_percent_rank_2,
         'mean_da2_matched_average_rank': mean_da2_matched_average_rank,
         'mean_da2_matched_right_matched':mean_da2_matched_right_matched,
         'mean_da2_matched_under_matched':mean_da2_matched_under_matched,
         'mean_da2_matched_over_matched':mean_da2_matched_over_matched,
         'mean_da3_matched_student_percent': mean_da3_matched_student_percent,
         'mean_da3_matched_percent_rank_1': mean_da3_matched_percent_rank_1,
         'mean_da3_matched_percent_rank_2': mean_da3_matched_percent_rank_2,
         'mean_da3_matched_average_rank': mean_da3_matched_average_rank,
         'mean_da3_matched_right_matched':mean_da3_matched_right_matched,
         'mean_da3_matched_under_matched':mean_da3_matched_under_matched,
         'mean_da3_matched_over_matched':mean_da3_matched_over_matched
          }

    d2 = pd.DataFrame(mean_da1_matched_score_min)
    d2 = pd.concat([d2, pd.DataFrame(mean_da1_matched_score_mean)], axis=1)
    d2 = pd.concat([d2, pd.DataFrame(mean_da1_matched_score_std)], axis=1)

    d3 = pd.DataFrame(mean_da2_matched_score_min)
    d3 = pd.concat([d3, pd.DataFrame(mean_da2_matched_score_mean)], axis=1)
    d3 = pd.concat([d3, pd.DataFrame(mean_da2_matched_score_std)], axis=1)

    d4 = pd.DataFrame(mean_da3_matched_score_min)
    d4 = pd.concat([d4, pd.DataFrame(mean_da3_matched_score_mean)], axis=1)
    d4 = pd.concat([d4, pd.DataFrame(mean_da3_matched_score_std)], axis=1)

    result = pd.DataFrame(d1)
    result.to_excel('result3.xlsx')
    d2.to_excel('result3_d2.xlsx')
    d3.to_excel('result3_d3.xlsx')
    d4.to_excel('result3_d4.xlsx')