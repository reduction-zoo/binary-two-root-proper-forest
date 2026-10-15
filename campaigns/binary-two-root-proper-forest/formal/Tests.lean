import Challenge
open BinaryTwoRootProperForest
example : legalTarget ⟨7,[(0,2),(0,3),(1,2),(1,4),(2,5),(3,6)]⟩ = false := by native_decide
example : targetWitness ⟨3,[(0,2),(1,2)]⟩ [(0,2)] = false := by native_decide
example : targetWitness ⟨4,[(0,2),(1,3)]⟩ [(0,2),(1,3)] = true := by native_decide

example : legalTarget ⟨6,[(0,2),(0,4),(1,2),(1,5),(2,3)]⟩ = true := by native_decide
example : targetWitness ⟨6,[(0,2),(0,4),(1,2),(1,5),(2,3)]⟩ [(0,2),(0,4),(1,5),(2,3)] = true := by native_decide
