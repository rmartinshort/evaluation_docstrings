import heapq


class Solution(object):
    def assignBikes(self, workers, bikes):
        bike_distances = []
        heap = []
        for i, worker in enumerate(workers):
            curr_worker_pairs = []
            for j, bike in enumerate(bikes):
                # get all the pairs i->j and j->i
                curr_worker_pairs.append((self.distance(worker, bike), i, j))

            # sort so that we can pop this to get the closest distance
            curr_worker_pairs.sort(reverse=True)
            # add closest bike to this worker to the heap
            heapq.heappush(heap, curr_worker_pairs.pop())
            # store remaining options for this worker in a list
            bike_distances.append(curr_worker_pairs)

        # keep track of which worker is assigned to bikes
        bike_status = [False] * len(bikes)
        # keep track of which bike is assigned to each worker
        worker_status = [None] * len(workers)

        while heap:
            # get shortest distance
            distince, worker, bike = heapq.heappop(heap)

            # if that bike is not taken, take it
            if not bike_status[bike]:
                bike_status[bike] = True
                worker_status[worker] = bike
            # get the next closest bike
            else:
                next_closest_bike = bike_distances[worker].pop()
                heapq.heappush(heap, next_closest_bike)

        return worker_status

        print(bike_distances)

        res = []
        while bike_distances:
            res.append(heapq.heappop(bike_distances)[1:])
        return res

    @staticmethod
    def distance(worker, bike):
        return abs(worker[0] - bike[0]) + abs(worker[1] - bike[1])
