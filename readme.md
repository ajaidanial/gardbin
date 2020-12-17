# gardbin

Some random algorithm that gets a text file and uses PostgreSQL to store the data.

## Getting Started
1. Clone and `cd` to file(project root).
2. Make sure the input file is in the project root.  
3. Add necessary configurations in `config.json`.  
4. Use `./start.sh`  

## Setting Up CRON
1. Run the command `*/5 * * * * ./start.sh` to set up for every 5 minutes.  
2. For more CRON configurations view [here](https://www.thegeekstuff.com/2011/07/cron-every-5-minutes/).  
