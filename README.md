# An improved Uniprot download script

If we copy paste the scripts from [Uniprot's official help page](https://www.uniprot.org/help/api_queries#22-large-number-of-results-use-pagination), we would occasionally run into errors that would propagate "Error encountered when streaming data. Please try again later." straight into the streamed file.

This script sort of handles that case.

Besides the above error, I did not run into any more issues yet.

## Example

The current URL and slurm script downloads all sequences returned by the "protease" query. 

For your use case, modify the `url` in `uniprot_dl.py` and the `--job-name`, `--output` and `--error` flags in `download.slurm.sh`. 

Of course, if you are not using slurm, just call 

```
python uniprot_dl.py
```
