using System.IO.Ports;
using System.Threading;
using System;
using System.IO;
using System.Diagnostics;

class Program
{
    static SerialPort sp;
    static bool _continue;

    static void Main(string[] args)
    {
        string name;
        string message;
        StringComparer stringComparer = StringComparer.OrdinalIgnoreCase;

        // Create a new SerialPort object with default settings.
        sp = new SerialPort();

        // Allow the user to set the appropriate properties.
        sp.PortName = SetPortName();
        sp.Handshake = SetPortHandshake();
        sp.BaudRate = SetPortBaudRate(sp.BaudRate);
        sp.Parity = SetPortParity();
        sp.DataBits = SetPortDataBits(sp.DataBits);
        sp.StopBits = SetPortStopBits();
        sp.DataReceived += new SerialDataReceivedEventHandler(sp_DataReceived);

        // Set the read/write timeouts
        sp.ReadTimeout = 500;
        sp.WriteTimeout = 1000;

        try
        {
            sp.Open();
        }
        catch (IOException ex)
        {
            Console.WriteLine(ex.ToString());
        }

        _continue = true;
        name = sp.PortName;

        Console.WriteLine("\nType message (QUIT to exit):");

        while (_continue)
        {
            message = Console.ReadLine();

            if (stringComparer.Equals("quit", message))
            {
                _continue = false;
            }
            else
            {
                sp.WriteLine(
                    String.Format("<{0}>: {1}", name, message));
            }
        }

    }

    public static void sp_DataReceived(object sender, SerialDataReceivedEventArgs e)
    {

        while (_continue)
        {
            Thread.Sleep(5000);
            try
            {
                string message = sp.ReadLine();
                Console.WriteLine(message);
            }
            catch (TimeoutException)
            {
                Debug.WriteLine($"Read {sp.PortName.ToString()} Timeout");
            }
        }
    }

    // Display Port values and prompt user to enter a port.
    public static string SetPortName()
    {
        var ports = SerialPort.GetPortNames();

        Console.WriteLine("Available Ports:");

        for (int j = 0; j < ports.Length; j++)
            Console.WriteLine("{0}.   {1}", j, ports[j]);

        Console.Write("Enter COM port value: ");

        int i;
        do
        {
            i = Convert.ToInt32(Console.ReadLine());
        }
        while (i < 0 || i >= ports.Length);

        return ports[i];
    }

    public static Handshake SetPortHandshake()
    {
        var handshakes = Enum.GetNames(typeof(Handshake));

        Console.WriteLine("\nAvailable Handshake options:");
        for (int i = 0; i < handshakes.Length; i++)
        {
            Console.WriteLine("{0}. {1}", i, handshakes[i]);
        }

        Console.Write("Enter Handshake value: ");

        int j;
        do
        {
            j = Convert.ToInt32(Console.ReadLine());
        }
        while (j < 0 || j >= handshakes.Length);

        return (Handshake)Enum.Parse(typeof(Handshake), handshakes[j], true);
    }

    // Display BaudRate values and prompt user to enter a value.
    public static int SetPortBaudRate(int defaultPortBaudRate)
    {
        string baudRate;

        Console.Write("\nEnter Baud Rate (default:{0}): ", defaultPortBaudRate);
        baudRate = Console.ReadLine();

        if (baudRate == "")
        {
            baudRate = defaultPortBaudRate.ToString();
        }

        return int.Parse(baudRate);
    }


    public static Parity SetPortParity()
    {
        var parities = Enum.GetNames(typeof(Parity));

        Console.WriteLine("\nAvailable Parity options:");

        for (int j = 0; j < parities.Length; j++)
            Console.WriteLine("{0}.   {1}", j, parities[j]);

        Console.Write("Enter Parity value: ");

        int i;
        do
        {
            i = Convert.ToInt32(Console.ReadLine());
        }
        while (i < 0 || i >= parities.Length);

        return (Parity)Enum.Parse(typeof(Parity), parities[i], true);
    }

    public static int SetPortDataBits(int default_databits)
    {
        string databits;
        Console.Write("\nEnter Databits value (5-8, default: {0}): ", default_databits);
        databits = Console.ReadLine();

        if (databits == "")
            databits = default_databits.ToString();

        return Convert.ToInt32(databits.ToUpperInvariant());
    }

    public static StopBits SetPortStopBits()
    {
        var stopbits = Enum.GetNames(typeof(StopBits));
        Console.Write("\nAvailable Stopbits value (None is not supported)\n");
        for (int i = 1; i < stopbits.Length; i++)
            Console.WriteLine("{0}.   {1}", i, stopbits[i]);

        int stopbits_index;
        Console.Write("Enter StopBits value: ");
        do
        {
            stopbits_index = Convert.ToInt32(Console.ReadLine());
        }
        while (stopbits_index < 0 || stopbits_index >= stopbits.Length);

        return (StopBits)Enum.Parse(typeof(StopBits), stopbits[stopbits_index], true);
    }
}