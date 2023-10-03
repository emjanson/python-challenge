import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) #sets the working directory to the directory that the script is currently located
os.chdir(script_dir)

#create a new file output directory 'analysis' in the script directory if it does not exist
file_output_dir = os.path.join(script_dir, 'analysis')
if not os.path.exists(file_output_dir):
    os.mkdir(file_output_dir)

#name the output files and output file paths
budget_output_file = 'budget_calculations_output.txt'
election_output_file = 'election_tabulation_output.txt'
output_file_path_budget = os.path.join(file_output_dir, budget_output_file)
output_file_path_election = os.path.join(file_output_dir, election_output_file)

#point to the input files
csv_path_budget = os.path.join(script_dir, 'Resources', 'budget_data.csv') #points to the data file in subdirectory 'Resources' in the script working directory
csv_path_election = os.path.join(script_dir, 'Resources', 'election_data.csv')

#define a special function to output to the terminal and to a text file simultaneously
def print_to_term_and_write_to_file(text, file): 
    print(text)
    file.write(text + '\n')
    
#define variables needed for budget calculations 
total_profit_loss = 0
number_of_months = 0
monthly_profit_loss = 0
highest_profit = 0
highest_loss = 0
monthly_diff = 0
previous_month_profit_loss = None
highest_profit_month = None
highest_loss_month = None
monthly_differences_list = []

with open(csv_path_budget, 'r', encoding='UTF-8') as csv_file:  #open the CSV file from the Resources directory
    
    csv_reader = csv.DictReader(csv_file, delimiter=',') #create an reader object using DictReader class (of CSV module) to extract column headers from the first row of the CSV file
  
    for row in csv_reader:
        
        #for each row in the CSV file that had data under the column header 'Date' add 1 to the month total counter  
        if 'Date' in row:
            number_of_months += 1
            
        #for each row in the CSV file that has data under the column header 'Profit/Losses' add to a running sum to calculate total profit and losses over the entire dataset    
        if 'Profit/Losses' in row:          
            total_profit_loss += float(row['Profit/Losses'])
            monthly_profit_loss = float(row['Profit/Losses']) #sends the profits/losses data for each row to a variabe for further calculations
    
        if previous_month_profit_loss is not None: #check to make sure the previous profits/losses row contains data (the first row of data will have no previous month to compare to since it is the first entry in the CSV file)
            monthly_diff = monthly_profit_loss - previous_month_profit_loss  #subtract previous row profit/loss from current row profit/loss to find the month to month difference
            monthly_differences_list.append(monthly_diff)  #append the current month to month profit/loss difference to a list that stores all the month to month profit/loss differences for later overall monthly profit/loss mean (average) calculation
       
        #this if/elif section stores the highest and lowest monthly profit/loss differences and the corresponding date information
        if  monthly_diff > highest_profit:  
            highest_profit = monthly_diff
            highest_profit_month = str(row['Date'])
        elif monthly_diff < highest_loss:
            highest_loss = monthly_diff
            highest_loss_month = str(row['Date'])
            
        previous_month_profit_loss = monthly_profit_loss #before moving to the next row, set the previous month profit/loss variable to the current row profit/loss value

    mean_monthly_diff = float(sum(monthly_differences_list)) / (number_of_months - 1) #calculate the mean month to month profit/loss from the list of monthly differences we stored as we iterated through the rows

#round all of the output variables to desired number of decimal places
rounded_mean_monthly_diff = round(mean_monthly_diff, 2)
rounded_total_profit_loss = round(total_profit_loss, 0)
rounded_highest_loss = round(highest_loss, 0)
rounded_highest_profit = round(highest_profit, 0)

#print all of the desired outputs to the terminal and send the data to a text file        
with open(output_file_path_budget, "w") as file:
    print()
    print_to_term_and_write_to_file("Financial Analysis", file)
    print_to_term_and_write_to_file("-------------------------", file)
    print_to_term_and_write_to_file(f"Total Months: {number_of_months}", file)
    print_to_term_and_write_to_file(f"Total: ${rounded_total_profit_loss:.0f}", file)
    print_to_term_and_write_to_file(f"Average Change: ${rounded_mean_monthly_diff}", file)
    print_to_term_and_write_to_file(f"Greatest Increase in Profits: {highest_profit_month} (${rounded_highest_profit:.0f})", file)
    print_to_term_and_write_to_file(f"Greatest Decrease in Profits: {highest_loss_month} (${rounded_highest_loss:.0f})", file)
    
#define variables needed for ballot tabulations
unique_candidates = {} #create a dictionary to store the unique candidate names
candidate_name = None #variable for use in summing vote totals for each unique candidate
number_of_ballots = 0  #variabe for storing the number of total ballots
top_vote_getter = None #variable for storing candidate name with most votes
top_vote_getter_counts = 0 #variable for storing the vote counts for the candidate with most votes

with open(csv_path_election, 'r', encoding='UTF-8') as csv_file:  #open the CSV file from the Resources directory
    
    csv_reader = csv.DictReader(csv_file, delimiter=',') #create an reader object using DictReader class (of CSV module) to extract column headers from the first row of the CSV file
    
    for row in csv_reader:   
        
        #if statement for counting overall ballot total
        if 'Ballot ID' in row:  
            number_of_ballots += 1
        
        # if statement for counting ballot totals for each unique candidate    
        candidate_name = row['Candidate']   
        if candidate_name in unique_candidates:
            unique_candidates[candidate_name] += 1
        else:
            unique_candidates[candidate_name] = 1
           
#printing all desired outputs to terminal and to file
with open(output_file_path_election, "w") as file:
    print()
    print_to_term_and_write_to_file("Election Results", file)
    print_to_term_and_write_to_file("-------------------------", file)
    print_to_term_and_write_to_file(f"Total Votes: {number_of_ballots}", file)
    print_to_term_and_write_to_file("-------------------------", file)
    
    #loop for printing the name of each individual unique candidate, their % of the total vote, and their total number of votes
    for candidate_name, unique_candidate_counts in unique_candidates.items():
        unique_candidate_percent_vote = (unique_candidate_counts / number_of_ballots) * 100
        rounded_unique_candidate_percent_vote = round(unique_candidate_percent_vote, 3)   #round the percentage of total votes to 3 decimal places
        
        #find which candidate received the most votes and therefore won the election
        if unique_candidate_counts > top_vote_getter_counts:
            top_vote_getter_counts = unique_candidate_counts
            top_vote_getter = candidate_name
            
        print_to_term_and_write_to_file(f"{candidate_name}: {rounded_unique_candidate_percent_vote}% ({unique_candidate_counts})", file)
    print_to_term_and_write_to_file("-------------------------", file)
    print_to_term_and_write_to_file(f"Winner: {top_vote_getter}", file)
    print_to_term_and_write_to_file("-------------------------", file)