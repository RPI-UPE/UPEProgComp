import collections

from django.conf import settings
from django.db.models import Min
from django.db.models import Q

from progcomp.submission.models import Submission
from progcomp.problems.models import Problem

# This is not a real relation in the database, it is just used as an accessor
class Scoreboard:
	@staticmethod
	def results():
		"""
		Returns a sorted list of users based on problems completed with ties broken
		at the last completion time. Additionally returns a list of tuples for problems
		with individual times and statuses.
		Return: [(User, num_completed, last_time, (problem_1_time, ...)), ...]
		"""
		# Get all submissions
		all_submissions = Submission.objects.all() \
				.values_list('registrant', 'attempt__problem', 'submitted', 'result__status') \
				.extra(order_by=['-result__status', 'submitted'])

		# Get problem set and respective best times
		problem_set = Problem.objects \
			.filter(Q(attempt__submission__result__status='success') | \
					Q(attempt__submission__result__status__isnull=True)) \
			.annotate(best_time=Min('attempt__submission__submitted'))
		problem_set = dict([[p.id, p] for p in problem_set])

		# Build dictionary of users mapped to problems mapped to time completed
		users = collections.defaultdict(dict)
		for user, problem, dt, status in all_submissions:
			if status == 'success':
				# If it is a successful result, take the first (earliest) we find and ignore the rest
				if problem not in users[user]:
					# Check for late submissions
					if dt > settings.END:
						status = 'invalid'
					# Check for first submissions for a given problem
					if dt == problem_set[problem].best_time:
						status += ' first'
					users[user][problem] = (dt, status)
			elif not problem in users[user] or users[user][problem][1] == 'failed':
				# If they were not successful, take the most recent failed attempt
				users[user][problem] = (dt, 'failed')

		# Summarize dict for sorting by rank (num_correct, latest_time, user)
		ranks = []
		for user, problems in users.items():
			number_submitted = sum(1 for t, st in problems.values() if st.startswith('success'))
			# Use try/except in case they have no successful attempts
			try:
				max_time = max(t for t, st in problems.values() if st.startswith('success'))
			except:
				# This is more or less arbitrary to maintain order amongst those who solved 0
				max_time = max(t for t, st in problems.values())
			ranks.append( (number_submitted, max_time, user) )
		# Comparison function for finding the winner
		def comp(lhs, rhs):
			if lhs[0] == rhs[0]:
				return cmp(lhs[1], rhs[1])
			return -cmp(lhs[0], rhs[0])
		ranks.sort(comp)

		# Given a user id, return a list of times said user completed each
		# problem, or None in place if user has not yet completed
		def user_solns(user):
			# Store solution as a list of tuples with incomplete being None
			# First take the dict of what we solved and convert it into a list filling in gaps
			solns = users[user]
			return [i in solns and solns[i] or (None, None) for i in [id for id in problem_set]]

		# Format for templater
		ranks = map(lambda y: (y[2], y[0], y[1], user_solns(y[2])), ranks)

		return ranks, problem_set.values()
