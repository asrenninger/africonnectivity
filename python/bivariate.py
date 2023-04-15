def bivariate_choropleth(data, basemap, voi_1, voi_2, scheme, background='k', **kwargs):
    # set parameters if kwargs are not passed
    tit = kwargs.get('title', "")
    lb1 = kwargs.get('label1', "")
    lb2 = kwargs.get('label2', "")
    fnm = kwargs.get('fnm', "")
    pts = kwargs.get('pts', 1)
    lwd = kwargs.get('lwd', 1)

    # create a dataframe with the bivariate color scheme
    bivariate = pd.DataFrame(scheme)

    if background == 'k':
        foreground = 'w'
    else:
        foreground = 'k'

    # copy data
    ready = data.copy()

    # convert var_1 into 3  quantiles 
    ready['voi1_qtile'] = pd.qcut(ready[voi_1].rank(method='first'), 3, labels=["1", "2", "3"])

    # convert var_2 into 3 quantiles
    ready['voi2_qtile'] = pd.qcut(ready[voi_2].rank(method='first'), 3, labels=["1", "2", "3"])

    # # replace na values with the first quantile
    # ready['flow_qtile'] = ready['flow_qtile'].fillna("1")
    # ready['risk_qtile'] = ready['risk_qtile'].fillna("1")

    # join the two quantiles together
    ready['class'] = ready['voi2_qtile'].astype(str) + "-" + ready['voi1_qtile'].astype(str)

    # merge the bivariate color scheme with the data
    ready = ready.merge(bivariate, on='class')

    # create a matplotlib categorical color map with the bi-variate color scheme
    from matplotlib.colors import ListedColormap
    bmap = ListedColormap(bivariate['color'].values)

    # make fig and ax objects
    fig, ax = plt.subplots(1, 1, figsize=(20, 20), facecolor=background)

    # plot africa with no fill and dashed lines as a base layer
    basemap.to_crs(ready.crs).plot(color=background, edgecolor='#7c7c7c', linestyle='--', ax=ax)

    # plot it with the "class" column and use the categorical color map
    # joined.plot(color='w', ax=ax)
    if ready.geom_type[0] == 'LineString':
        ready.plot(column='class', linewidth=lwd, cmap=bmap, ax=ax)
    else:
        ready.sort_values(pts, ascending=False).plot(column='class', cmap=bmap, ax=ax, markersize=np.sqrt(ready[pts] / 10))

    # clean it up
    ax.set_facecolor(background)
    ax.set_title(tit, color=foreground, size=20, weight='bold')
    ax.set_axis_off()

    # make a subplot in the bottom left corner
    sub = fig.add_axes([0.25, 0.3, 0.15, 0.15])

    sub.imshow(np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]]), cmap=bmap)

    # turn it 90 degrees
    sub.set_xticks([])
    sub.set_yticks([])
    sub.set_xticklabels([])
    sub.set_yticklabels([])
    sub.set_frame_on(False)
    sub.invert_yaxis()
    sub.set_aspect('equal')

    # add axis titles
    sub.text(0.5, -0.1, lb1 + u"\u2192", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=15, color=foreground)
    sub.text(-0.1, 0.5, lb2 + u"\u2192", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=15, rotation=90, color=foreground)

    # # save this plot as a high resolution png
    if fnm != "":
        plt.savefig(fnm, dpi=300, bbox_inches='tight', pad_inches=0)