import pickle
import os
import re




def save_obj(obj,name):
    try:
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f)
    except FileNotFoundError:
       raise FileNotFoundError

def load_obj(name):
    try:
        with open( name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("FileNotFoundError on load")
        return {}
    except EOFError:
        print("EOFError on load")
        return {}                          

def get_running_total(name):
    global_scores = load_obj(name)
    if "top_score" not in global_scores.keys():
        global_scores["top_score"]=0
    if "total_iterations" not in global_scores.keys():
        global_scores["total_iterations"]=0
    if "top_score_summary" not in global_scores.keys():
            global_scores["top_score_summary"]=""

    print("----------------------------------")
    print("Global Top Score: "+str(global_scores["top_score"]))
    print("\tSummary: "+str(global_scores["top_score_summary"]))
    print("Total Iterations: "+str(global_scores["total_iterations"]))
    print("----------------------------------")
    return global_scores

def set_new_max(name,global_scores,score,summary,i,model=None):
    if score > global_scores["top_score"]:
        if "top_score" not in global_scores.keys():
            global_scores["top_score"]=0
        if "total_iterations" not in global_scores.keys():
            global_scores["total_iterations"]=0

        global_scores["top_model"]=model


        global_scores["top_score"]=score
        global_scores["top_score_summary"]="Global"+summary
        print("----------------------------------")
        print("\tNew Global Top Score: "+str(global_scores["top_score"]))
        print("\t\tSummary: "+str(global_scores["top_score_summary"]))
        print("\tIterations: "+str(i+global_scores["total_iterations"]))
        
        print("----------------------------------")
        global_scores["total_iterations"]=global_scores["total_iterations"]+i
        save_obj(global_scores,name)
        return global_scores

def save_iteration_count(name,global_scores,i):
    global_scores["total_iterations"]=global_scores["total_iterations"]+i
    save_obj(global_scores,name)
    return global_scores

def get_best_model(name):
    global_scores = load_obj(name)
    if "top_model" in global_scores.keys():
        return global_scores["top_model"]
    else:
        return None