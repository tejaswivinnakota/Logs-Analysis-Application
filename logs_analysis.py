import psycopg2

DBNAME = "news"

get_three_popular_articles = """Select title, count(modified_log.id) as num from articles, (Select substring(path, '[^/]*$') as slug, id from log) as modified_log where articles.slug = modified_log.slug group by title order by num desc limit 3"""
# Returns 3 most popular articles from the 'database', most popular first.

get_popular_authors = """Select name, num from authors, (Select author, count(modified_log.id) as num from articles, (Select substring(path, '[^/]*$') as slug, id from log) as modified_log where articles.slug = modified_log.slug group by author) as pop_auth_ids where authors.id = pop_auth_ids.author order by num desc"""
# Returns most popular authors from the 'database', most popular first.

get_days_error_rate_more_than_one = """Select date, pct from (Select sub_tot.date as date, round(sub_tot.sum :: decimal / tot.sum :: decimal * 100,2) as pct from(Select to_char(time, 'Month DD, YYYY') as date, count(id) as sum from log group by date) as tot, (Select to_char(time, 'Month DD, YYYY') as date, count(id) as sum from log where status like '4%' OR status like '5%' group by date) as sub_tot where tot.date = sub_tot.date) as req where req.pct > 1"""
# Returns days with error rate more than 1 from the 'database'.

print("\n\t\t--- LOGS ANALYSIS ---\n")

def get_results(query):
  # Returns results from the 'database', as per the query.
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(query)
  results =  c.fetchall()
  db.close()
  return results
  
  
  
def view_three_popular_articles():
# Prints 3 most popular articles from the 'database', most popular first.
  three_popular_articles = get_results(get_three_popular_articles)
  print("\n\t\tThree popular articles of all time\n")
  for title, num in three_popular_articles:
    print(" \"{}\" -- {} views".format(title, num))



def view_popular_authors():
# Prints most popular authors from the 'database', most popular first.
  popular_authors = get_results(get_popular_authors)
  print("\n\t\tPopular authors of all time\n")
  for name, num in popular_authors:
    print(" {} -- {} views".format(name, num))

	
def view_days_error_rate_more_than_one():
# Prints days with error rate more than 1 from the 'database'.
  days_error_rate_more_than_one = get_results(get_days_error_rate_more_than_one)
  print("\n\t\tDays with error rate more than one\n")
  for date, percent in days_error_rate_more_than_one:
    print(" {} -- {}% errors".format(date, percent))


if __name__ == '__main__':
  view_three_popular_articles()
  view_popular_authors()
  view_days_error_rate_more_than_one()
