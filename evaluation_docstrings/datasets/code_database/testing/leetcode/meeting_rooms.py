class Solution(object):
    def canAttendMeetings(self, intervals):
        intervals.sort(key=lambda x: x[1])

        # print(intervals)

        last_meeting_end = 0
        for meeting in intervals:
            meeting_start = meeting[0]
            if meeting_start < last_meeting_end:
                return False
            last_meeting_end = meeting[1]

        return True
