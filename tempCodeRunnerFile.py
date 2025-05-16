lm_l = Lasso()
np.mean(cross_val_score(lm_l,x_train,y_train, scoring = 'neg_mean_absolute_error', CV = 3))


## Create 2 empty list for alpha and error
alpha = []
error = []

## plot the alpha
for i in range (1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml,x_train,y_train, scoring = 'neg_mean_absolute_error')))

plt.plot(alpha, error)