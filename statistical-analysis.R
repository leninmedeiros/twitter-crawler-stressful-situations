# Analysis for the first part of the experiment where people provided answers via a multiple choice question. - BEGIN
death = matrix(c(31,20,62,3,18), byrow=TRUE, ncol=5)
rownames(death) = c("Death")
colnames(death) = c("AD","CC","GES","SM","SS")

finances = matrix(c(24,45,24,26,19), byrow=TRUE, ncol=5)
rownames(finances) = c("Finances")
colnames(finances) = c("AD","CC","GES","SM","SS")

health = matrix(c(18,34,69,6,11), byrow=TRUE, ncol=5)
rownames(health) = c("Health")
colnames(health) = c("AD","CC","GES","SM","SS")

relationships = matrix(c(40,26,20,19,26), byrow=TRUE, ncol=5)
rownames(relationships) = c("Relationships")
colnames(relationships) = c("AD","CC","GES","SM","SS")

school = matrix(c(26,59,23,23,9), byrow=TRUE, ncol=5)
rownames(school) = c("School")
colnames(school) = c("AD","CC","GES","SM","SS")

work = matrix(c(28,56,25,17,8), byrow=TRUE, ncol=5)
rownames(work) = c("Work")
colnames(work) = c("AD","CC","GES","SM","SS")

chisq.test(death)
chisq.test(finances)
chisq.test(health)
chisq.test(relationships)
chisq.test(school)
chisq.test(work)

# To continue with the simulations!!!
simulation_death = replicate(n = 2000000, sample( c("AD","CC","GES","SM","SS"), size = 134, replace = T))
# Analysis for the first part of the experiment where people provided answers via a multiple choice question. - END

# Analysis for the second part of the experiment where people provided answers via a multiple choice question. - BEGIN
death = matrix(c(24,10,219,9,7,17), byrow=TRUE, ncol=6)
rownames(death) = c("Death")
colnames(death) = c("AD","CC","GES","SM","SS","NONE")

finances = matrix(c(53,40,82,67,13,19), byrow=TRUE, ncol=6)
rownames(finances) = c("Death")
colnames(finances) = c("AD","CC","GES","SM","SS","NONE")

health = matrix(c(33,38,162,28,5,17), byrow=TRUE, ncol=6)
rownames(health) = c("Death")
colnames(health) = c("AD","CC","GES","SM","SS","NONE")

relationships = matrix(c(54,63,98,31,16,18), byrow=TRUE, ncol=6)
rownames(relationships) = c("Death")
colnames(relationships) = c("AD","CC","GES","SM","SS","NONE")

school = matrix(c(54,123,57,47,14,13), byrow=TRUE, ncol=6)
rownames(school) = c("Death")
colnames(school) = c("AD","CC","GES","SM","SS","NONE")

work = matrix(c(45,84,61,55,21,15), byrow=TRUE, ncol=6)
rownames(work) = c("Death")
colnames(work) = c("AD","CC","GES","SM","SS","NONE")

chisq.test(death)
chisq.test(finances)
chisq.test(health)
chisq.test(relationships)
chisq.test(school)
chisq.test(work)
# Analysis for the second part of the experiment where people provided answers via a multiple choice question. - END
