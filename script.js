// <!-- JavaScript for displaying date and time -->
    
        const currentDate = new Date();
        document.getElementById('date').innerHTML = currentDate.toDateString();
        setInterval(() => {
            const currentTime = new Date();
            document.getElementById('time').innerHTML = currentTime.toLocaleTimeString();
        }, 1000);
    
    // <!-- end of this script -->

    // search product name for supplier

    


