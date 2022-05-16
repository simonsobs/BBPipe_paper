# BB pipeline paper plots

To add a new plot:
- Add all necessary data to the `data` folder. Be minimalistic (e.g. if you are taking the mean and standard deviation of 500 sims and only using that in the plot, then it's best to just upload a file with the mean and standard deviation, than 500 files with all the sims).
- Add a script to `plot_scripts` that uses those data to generate a plot. It should be callable from the root directory. See [plot_scripts/example.py](plot_scripts/example.py) for an example.
- Do not add the plot this generates to the repo. pdf files are not easy to track for git, and they end up taking a huge amount of space.
