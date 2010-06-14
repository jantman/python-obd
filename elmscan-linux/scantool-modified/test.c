#include <string.h>
#include <ctype.h>
#include "globals.h"
#include <dzcomm.h>

static comm_port *com_port;

int main()
{
   char temp_buf[64];
   time_t current_time;
   
   time(&current_time);  // get current time, and store it in current_time
   strcpy(temp_buf, ctime(&current_time));
   temp_buf[strlen(temp_buf)-1] = 0;
   
   strcpy(log_file_name, "log.txt");
   remove(log_file_name);
   write_log(temp_buf);
   strcpy(comm_log_file_name, "comm_log.txt");
   remove(comm_log_file_name);
   write_comm_log("START_TIME", temp_buf);

   sprintf(temp_buf, "\nVersion: %s for %s", SCANTOOL_VERSION_STR, SCANTOOL_PLATFORM_STR);
   write_log(temp_buf);

   write_log("\n\nInitializing All Modules...\n---------------------------");
   init(); // initialize everything

   // TODO - do stuff here!!
   printf("DO STUFF.");

   write_log("\n\nShutting Down All Modules...\n----------------------------");
   shut_down(); // shut down

   return EXIT_SUCCESS;
}

static void init()
{
   char temp_buf[256];

   is_not_genuine_scan_tool = FALSE;
   
   /* initialize some varaibles with default values */
   strcpy(options_file_name, "scantool.cfg");
   strcpy(data_file_name, "scantool.dat");
   strcpy(code_defs_file_name, "codes.dat");
   
   datafile = NULL;
   comport.status = NOT_OPEN;

   set_uformat(U_ASCII);
   
//   write_log("\nInstalling Timers... ");
//   if (install_timer() != 0)
//   {
//      write_log("Error!");
//      fatal_error("Error installing timers");
//   }
//   write_log("OK");

   /* load options from file, the defaults will be automatically substituted if file does not exist */
   write_log("\nLoading Preferences... ");
   set_config_file(options_file_name);
   load_program_options();
   /* if config file doesn't exist or is of an incorrect version */
   if (strcmp(get_config_string(NULL, "version", ""), SCANTOOL_VERSION_STR) != 0)
   {
      /* update config file */
      remove(options_file_name);
      set_config_file(options_file_name);
      set_config_string(NULL, "version", SCANTOOL_VERSION_STR);
      save_program_options();
   }
   write_log("OK");

   write_log("\nInitializing Serial Module... ");
   serial_module_init();
   write_log("OK");

   sprintf(temp_buf, "\nOpening COM%i... ", comport.number + 1);
   write_log(temp_buf);
   /* try opening comport (comport.status will be set) */
   open_comport();
   switch (comport.status)
   {
      case READY:
         write_log("OK");
         break;

      case NOT_OPEN:
         write_log("Error!");
         break;
         
      default:
         write_log("Unknown Status");
         break;
   }
}


static void shut_down()
{
   //clean up
   flush_config_file();
   write_log("\nShutting Down Serial Module... ");
   serial_module_shutdown();
   write_log("OK");
   write_log("\nUnloading Data File... ");
   unload_datafile(datafile);
   write_log("OK");
   write_log("\nShutting Down Allegro... ");
   allegro_exit();
   write_log("OK");
}



void serial_module_init()
{
   dzcomm_init();
   serial_timer_running = FALSE;
   /* all variables and code used inside interrupt handlers must be locked */
   LOCK_VARIABLE(serial_time_out);
   LOCK_FUNCTION(serial_time_out_handler);
}


void serial_module_shutdown()
{
   close_comport();
}

int open_comport()
{
   if (comport.status == READY)    // if the comport is open,
      close_comport();    // close it


   com_port = comm_port_init(comport.number);
   comm_port_set_baud_rate(com_port, comport.baud_rate);
   comm_port_set_parity(com_port, NO_PARITY);
   comm_port_set_data_bits(com_port, BITS_8);
   comm_port_set_stop_bits(com_port, STOP_1);
   comm_port_set_flow_control(com_port, NO_CONTROL);
   if (comm_port_install_handler(com_port) != 1)
   {
      comport.status = NOT_OPEN; //port was not open
      return -1; // return error
   }

   serial_time_out = FALSE;
   comport.status = READY;
   
   return 0; // everything is okay
}


void close_comport()
{
   if (comport.status == READY)    // if the comport is open, close it
   {
      comm_port_flush_output(com_port);
      comm_port_flush_input(com_port);
      comm_port_uninstall(com_port);
   }
   comport.status = NOT_OPEN;
}


void send_command(const char *command)
{
   char tx_buf[32];
   
   sprintf(tx_buf, "%s\r", command);  // Append CR to the command

   write_comm_log("TX", tx_buf);

   comm_port_flush_output(com_port);
   comm_port_flush_input(com_port);
   comm_port_string_send(com_port, tx_buf);
}


int read_comport(char *response)
{
   char *prompt_pos = NULL;

   int i = 0;
   
   while((response[i] = comm_port_test(com_port)) != -1) // while the serial buffer is not empty, read comport
      i++;
   response[i] = '\0'; // terminate string, erase -1
   
   prompt_pos = strchr(response, '>');

   if (prompt_pos != NULL)
   {
      write_comm_log("RX", response);
      *prompt_pos = '\0'; // erase ">"
      return PROMPT;      // command prompt detected
   }
   else if (strlen(response) == 0)  // if the string is empty,
      return EMPTY;
   else                         //otherwise,
   {
      write_comm_log("RX", response);
      return DATA;
   }
}
