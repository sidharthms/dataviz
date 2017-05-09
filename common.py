import json
import numpy as np
from collections import defaultdict

def load_data(file_path, splits, req=False):
    with open(file_path,"r", encoding='utf-8') as fp:
        data = json.load(fp)          # loads the json file
        numassigns = len(data["assignments"])
        numstudents = len(data["students"])

        scores_matrices = []
        time_matrices = []
        lengths_matrices = []
        student_names = []

        splits = [0] + splits
        splits.append(numassigns)
        for s in range(len(splits)-1):
            scores_matrices.append(np.zeros((numstudents, splits[s+1] - splits[s])))
            time_matrices.append(np.zeros((numstudents, splits[s+1] - splits[s])))
            lengths_matrices.append(np.zeros((numstudents, splits[s+1] - splits[s])))

        req_posts = []
        posts_req_dict = [[defaultdict(list), defaultdict(list)] for s in range(len(splits)-1)]
        postlengths_req_dict = [defaultdict(list) for s in range(len(splits)-1)]

        if req:
            for a in data["assignments"]:
                req_posts.append(a["prompted"])

        for s, student in enumerate(data["students"]):
            student_names.append(student["sortable_name"])

            for split in range(len(splits)-1):
                start = splits[split]
                end = splits[split+1]

                for a in range(end - start):
                    # scores
                    scores_matrices[split][s, a] = student["grades"][a + start]["score"]

                    # time
                    time_matrices[split][s, a] = student["grades"][a + start]["late"]

                    # lengths
                    total_length = 0
                    for p in student["grades"][a + start]["posts"]:
                        total_length += p["length"]
                    lengths_matrices[split][s, a] = total_length

                    if req:
                        if time_matrices[split][s, a] < 0:
                            posts_req_dict[split][0][req_posts[a + start]].append(len(student["grades"][a + start]["posts"]))
                        else:
                            posts_req_dict[split][1][req_posts[a + start]].append(len(student["grades"][a + start]["posts"]))
                            
                        postlengths_req_dict[split][req_posts[a + start]].append(total_length)

    return {
        'splits': splits,
        'student_names': student_names,
        'scores_matrices': scores_matrices,
        'time_matrices': time_matrices,
        'lengths_matrices': lengths_matrices,
        'posts_req_dict': posts_req_dict,
        'postlengths_req_dict': postlengths_req_dict,
    }
