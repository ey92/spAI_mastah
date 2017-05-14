import pickle
import numpy as np


if __name__ == "__main__":
	# with open("a.pkl", "rb") as f:
	#     w = pickle.load(f)

	# pickle.dump(w, open("a_py2.pkl","rb"), protocol=2)


	# In[ ]:
    with open('knowledge/sim_matrix1.pickle', 'rb') as f:
        # MATRIX_NUM = 1
        print("This is sim_matrix1")
        sim_matrix1 = pickle.load(f)
        # popMatrix(sim_matrix1,all_lemmas[:6459])
        pickle.dump(sim_matrix1, open('knowledge/sim_matrix1.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix2.pickle', 'rb') as f:
        # MATRIX_NUM = 2
        print("This is sim_matrix2")
        sim_matrix2 = pickle.load(f)
        # popMatrix(sim_matrix2,all_lemmas[6459+1:12918])
        pickle.dump(sim_matrix2, open('knowledge/sim_matrix2.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix3.pickle', 'rb') as f:
        # MATRIX_NUM = 3
        print("This is sim_matrix3")
        sim_matrix3 = pickle.load(f)
        # popMatrix(sim_matrix3,all_lemmas[12918+1:19377])
        pickle.dump(sim_matrix3, open('knowledge/sim_matrix3.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix4.pickle', 'rb') as f:
        # MATRIX_NUM = 4
        print("This is sim_matrix4")
        # sim_matrix4 = np.empty([400,6459])
        sim_matrix4 = pickle.load(f)
        # popMatrix(sim_matrix4,all_lemmas[19377+1:25836])
        pickle.dump(sim_matrix4, open('knowledge/sim_matrix4.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix5.pickle', 'rU') as f:
        # MATRIX_NUM = 5
        print("This is sim_matrix5")
        # sim_matrix5 = np.empty([400,6459])
        # file = f.read()
        # print(file)
        sim_matrix5 = pickle.load(f)
        # sim_matrix5 = pickle.loads(file)
        # popMatrix(sim_matrix5,all_lemmas[25836+1:32295])
        pickle.dump(sim_matrix5, open('knowledge/sim_matrix5.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix6.pickle', 'rb') as f:
        # MATRIX_NUM = 6
        print("This is sim_matrix6")
        # sim_matrix6 = np.empty([400,6459])
        sim_matrix6 = pickle.load(f)
        # popMatrix(sim_matrix6,all_lemmas[32295+1:38754])
        pickle.dump(sim_matrix6, open('knowledge/sim_matrix6.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix7.pickle', 'rb') as f:
        # MATRIX_NUM = 7
        print("This is sim_matrix7")
        # sim_matrix7 = np.empty([400,6459])
        sim_matrix7 = pickle.load(f)
        # popMatrix(sim_matrix7,all_lemmas[38754+1:45213])
        pickle.dump(sim_matrix7, open('knowledge/sim_matrix7.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix8.pickle', 'rb') as f:
        # MATRIX_NUM = 8
        print("This is sim_matrix8")
        sim_matrix8 = pickle.load(f)
        # popMatrix(sim_matrix8,all_lemmas[45213+1:51672])
        pickle.dump(sim_matrix8, open('knowledge/sim_matrix8.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix9.pickle', 'rb') as f:
        # MATRIX_NUM = 9
        print("This is sim_matrix9")
        sim_matrix9 = pickle.load(f)
        # popMatrix(sim_matrix9,all_lemmas[51672+1:58131])
        pickle.dump(sim_matrix9, open('knowledge/sim_matrix9.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix10.pickle', 'rb') as f:
        # MATRIX_NUM = 10
        print("This is sim_matrix10")
        sim_matrix10 = pickle.load(f)
        # popMatrix(sim_matrix10,all_lemmas[58131+1:64590])
        pickle.dump(sim_matrix10, open('knowledge/sim_matrix10.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix11.pickle', 'rb') as f:
        # MATRIX_NUM = 11
        print("This is sim_matrix11")
        sim_matrix11 = pickle.load(f)
        # popMatrix(sim_matrix11,all_lemmas[64590+1:71049])
        pickle.dump(sim_matrix11, open('knowledge/sim_matrix11.pickle', 'wb'), protocol=2)

    # In[ ]:
    with open('knowledge/sim_matrix12.pickle', 'rb') as f:
        # MATRIX_NUM = 12
        print("This is sim_matrix12")
        sim_matrix12 = pickle.load(f)
        # popMatrix(sim_matrix12,all_lemmas[71049+1:])
        pickle.dump(sim_matrix12, open('knowledge/sim_matrix12.pickle', 'wb'), protocol=2)
