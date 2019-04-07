from tf_workers import get_worker

Worker = get_worker('myworker')

worker_obj = Worker(number_of_pates_gists=int(input("Enter the number of pastes/gists fetches you want")),
                    match_patterns=[r".*\.(js|py|d)$", "RAMS*", "pass*", "U*", r".*?@domain.com"])

resp = worker_obj.run()
print(resp)