#!/bin/bash

#Variables
target="" #Ip
port_range="" #Port Range
auto_generate_report=false #HTML Report Parameter
scan_udp=false  #Enable UDP scan

#Function to handle errors
handle_error() {
    echo "An error occurred. Check the input parameters and try again."
    exit 1
}

#Stop the script with Ctrl+C
trap handle_error ERR

#Function to scan TCP ports using nmap
scan_ports_tcp() {
    if [ -z "$target" ] || [ -z "$port_range" ]; then
        read -p "Enter the IP or domain to scan: " target
        read -p "Enter the port range to scan (example: 1-1000): " port_range
    fi

    #Get the current date and time
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "Scanning TCP ports on $target..."

    #Add a header to scan_results.txt file
    echo "===== TCP SCAN: $timestamp =====" >> scan_results.txt
    echo "Target: $target" >> scan_results.txt
    echo "Port range: $port_range" >> scan_results.txt
    echo "--------------------------------" >> scan_results.txt

    #Run the commando nmap and capture output
    nmap_output=$(nmap -p $port_range -T4 $target)

    if [ $? -eq 0 ]; then
        echo "$nmap_output" >> scan_results.txt

        #Find open and closed ports
        open_ports=$(echo "$nmap_output" | grep -oP '\d+/tcp\s+open' | awk '{print $1}')
        closed_ports=$(echo "$nmap_output" | grep -oP '\d+/tcp\s+closed' | awk '{print $1}')

        #Display the results in the console and add to the report
        if [ -z "$open_ports" ]; then
            echo "No open TCP ports found on $target." >> scan_results.txt
            echo "No open TCP ports found on $target."
        else
            echo "Open TCP ports on $target: $open_ports" >> scan_results.txt
            echo "Open TCP ports on $target: $open_ports"
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed TCP ports found on $target." >> scan_results.txt
            echo "No closed TCP ports found on $target."
        else
            echo "Closed TCP ports on $target: $closed_ports" >> scan_results.txt
            echo "Closed TCP ports on $target: $closed_ports"
        fi
    else
        echo "Scan failed. Check the IP/Domain or port range." >> scan_results.txt
        echo "Scan failed. Check the IP/Domain or port range."
    fi

    echo "================================" >> scan_results.txt
    echo "" >> scan_results.txt

    if [ "$auto_generate_report" = true ]; then
        generate_report
    fi

    target=""
    port_range=""
}

#Function to scan UDP ports using nmap
scan_ports_udp() {
    if [ -z "$target" ] || [ -z "$port_range" ]; then
        read -p "Enter the IP or domain to scan: " target
        read -p "Enter the UDP port range to scan (example: 1-1000): " port_range
    fi

    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "Scanning UDP ports on $target..."

    echo "===== UDP SCAN: $timestamp =====" >> scan_results.txt
    echo "Target: $target" >> scan_results.txt
    echo "UDP Port range: $port_range" >> scan_results.txt
    echo "--------------------------------" >> scan_results.txt

    nmap_output=$(nmap -sU -p $port_range -T4 $target)

    if [ $? -eq 0 ]; then
        echo "$nmap_output" >> scan_results.txt

        open_ports=$(echo "$nmap_output" | grep -oP '\d+/udp\s+open' | awk '{print $1}')
        closed_ports=$(echo "$nmap_output" | grep -oP '\d+/udp\s+closed' | awk '{print $1}')

        if [ -z "$open_ports" ]; then
            echo "No open UDP ports found on $target." >> scan_results.txt
            echo "No open UDP ports found on $target."
        else
            echo "Open UDP ports on $target: $open_ports" >> scan_results.txt
            echo "Open UDP ports on $target: $open_ports"
        fi

        if [ -z "$closed_ports" ]; then
            echo "No closed UDP ports found on $target." >> scan_results.txt
            echo "No closed UDP ports found on $target."
        else
            echo "Closed UDP ports on $target: $closed_ports" >> scan_results.txt
            echo "Closed UDP ports on $target: $closed_ports"
        fi
    else
        echo "UDP scan failed. Check the IP/Domain or port range." >> scan_results.txt
        echo "UDP scan failed. Check the IP/Domain or port range."
    fi

    echo "================================" >> scan_results.txt
    echo "" >> scan_results.txt

    if [ "$auto_generate_report" = true ]; then
        generate_report
    fi

    target=""
    port_range=""
}

#Function to generate an HTML report
generate_report() {
    if [ ! -f scan_results.txt ]; then
        echo "No scan results available. Perform a scan first."
        return
    fi
    echo "Generating report..."
    echo "<html><body><h1>Port Scan Report</h1><pre>" > report.html
    cat scan_results.txt >> report.html
    echo "</pre></body></html>" >> report.html
    echo "Report generated: report.html"
}

#Function to analyze scan results
analyze_results() {
    if [ ! -f scan_results.txt ]; then
        echo "No scan results available. Perform a scan first."
        return
    fi
    echo "Analyzing results..."
    open_ports=$(grep -oP 'open' scan_results.txt | wc -l)
    closed_ports=$(grep -oP 'closed' scan_results.txt | wc -l)
    echo "Open ports: $open_ports"
    echo "Closed ports: $closed_ports"
}

#Function to clear previous result's files
clear_results() {
    rm -f scan_results.txt report.html
    echo "Previous results cleared."
}

#Function that displays the menu
show_menu() {
    echo ""
    echo "======= MENU ======="
    echo "1. Scan TCP ports"
    echo "2. Scan UDP ports"
    echo "3. Generate HTML report"
    echo "4. Analyze results"
    echo "5. Clear results"
    echo "6. Exit"
    echo "===================="
}

#Process the parameters
while getopts ":t:p:ru" opt; do
    case $opt in
        t) target="$OPTARG" ;; #IP or domain
        p) port_range="$OPTARG" ;; #Port range
        r) auto_generate_report=true ;; #Automatically generate the report
        u) scan_udp=true ;; #Enable UDP scan
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

#Check if input parameters were provided
if [ -n "$target" ] && [ -n "$port_range" ]; then
    if [ "$scan_udp" = true ]; then
        scan_ports_udp
    else
        scan_ports_tcp
    fi
    exit 0
fi

#Loop of the main menu
while true; do
    show_menu
    read -p "Choose an option: " choice
    case $choice in
        1)
            scan_ports_tcp
            ;;
        2)
            scan_ports_udp
            ;;
        3)
            generate_report
            ;;
        4)
            analyze_results
            ;;
        5)
            clear_results
            ;;
        6)
	    echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option, try again."
            ;;
    esac
done
