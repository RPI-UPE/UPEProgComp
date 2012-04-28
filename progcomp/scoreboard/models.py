import collections

from django.conf import settings

from progcomp.submission.models import Submission
from progcomp.problems.models import Problem

# This is not a real relation in the database, it is just used as an accessor
class Scoreboard:
	@staticmethod
	def results():
		"""
		Returns a sorted list of users based on problems completed with ties broken
		at the last completion time. Additionally returns a list of individual times.
		Return: [(User, num_completed, last_time, (problem_1_time, ...)), ...]
		"""
		# Get all submissions
		valid_submissions = Submission.objects.all() \
				.filter(result__status='success') \
				.values_list('registrant', 'attempt__problem', 'submitted') \
				.distinct()

		# Get problem set for size count and names
		problem_set = Problem.objects.all()

		# Build dictionary of users mapped to problems mapped to time completed
		best = dict([[p, None] for p in [p.id for p in problem_set]])
		users = collections.defaultdict(dict)
		for user, problem, dt in list(valid_submissions):
			if problem not in users[user] or users[user][problem] > dt:
				users[user][problem] = dt
			if not best[problem] or best[problem] > dt:
				best[problem] = dt

		# Summarize dict for sorting by rank (num_correct, latest_time, user)
		ranks = []
		for user, problems in users.items():
			number_submitted = sum(1 for t in problems.values() if t < settings.END)
			max_time = max(problems.values())
			ranks.append( (number_submitted, max_time, user) )
		def comp(lhs, rhs):
			if lhs[0] == rhs[0]:
				return cmp(lhs[1], rhs[1])
			return -cmp(lhs[0], rhs[0])
		ranks.sort(comp)

		# Given a user id, return a list of times said user completed each
		# problem, or None in place if user has not yet completed
		def user_solns(user):
			# Store solution as a list with incomplete being None
			solns = users[user]
			solns = [i in solns and solns[i] or None for i in [p.id for p in problem_set]]
			status = map(lambda y: (y[1] and y[1] > settings.END) and "invalid" or (y[1]==y[0] and "first" or None), zip(best.values(), solns))
			return zip(solns, status)

		ranks = map(lambda y: (y[2], y[0], y[1], user_solns(y[2])), ranks)

		return ranks, problem_set
