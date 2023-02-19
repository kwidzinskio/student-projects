/******************************************************
                  DirectShow .NET
		      netmaster@swissonline.ch
*******************************************************/
//				SampleGrabber MainForm

using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Collections;
using System.ComponentModel;
using System.Windows.Forms;
using System.Data;
using System.Runtime.InteropServices;
using System.IO;
using System.Diagnostics;

using DShowNET;
using DShowNET.Device;
using System.Threading;
using System.Reflection;

namespace SampleGrabberNET
{

/// <summary> Summary description for MainForm. </summary>
public class MainForm : System.Windows.Forms.Form, ISampleGrabberCB
{
	private System.Windows.Forms.Splitter splitter1;
	private System.Windows.Forms.ToolBar toolBar;
	private System.Windows.Forms.Panel videoPanel;
	private System.Windows.Forms.Panel stillPanel;
	private System.Windows.Forms.PictureBox pictureBox;
	private System.Windows.Forms.ToolBarButton toolBarBtnTune;
	private System.Windows.Forms.ToolBarButton toolBarBtnGrab;
	private System.Windows.Forms.ToolBarButton toolBarBtnSave;
	private System.Windows.Forms.ToolBarButton toolBarBtnSep;
	private System.Windows.Forms.ImageList imgListToolBar;
        private Label fps_counter;
        private ComboBox resolutionList;
        private System.ComponentModel.IContainer components;

	public MainForm()
	{
		// Required for Windows Form Designer support
		InitializeComponent();
	}

	/// <summary> Clean up any resources being used. </summary>
	protected override void Dispose( bool disposing )
	{
		if( disposing )
		{
			CloseInterfaces();
			
			if (components != null) 
			{
				components.Dispose();
			}
		}
		base.Dispose( disposing );
	}

		#region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.toolBar = new System.Windows.Forms.ToolBar();
            this.toolBarBtnTune = new System.Windows.Forms.ToolBarButton();
            this.toolBarBtnGrab = new System.Windows.Forms.ToolBarButton();
            this.toolBarBtnSep = new System.Windows.Forms.ToolBarButton();
            this.toolBarBtnSave = new System.Windows.Forms.ToolBarButton();
            this.imgListToolBar = new System.Windows.Forms.ImageList(this.components);
            this.videoPanel = new System.Windows.Forms.Panel();
            this.splitter1 = new System.Windows.Forms.Splitter();
            this.stillPanel = new System.Windows.Forms.Panel();
            this.fps_counter = new System.Windows.Forms.Label();
            this.pictureBox = new System.Windows.Forms.PictureBox();
            this.resolutionList = new System.Windows.Forms.ComboBox();
            this.stillPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).BeginInit();
            this.SuspendLayout();
            // 
            // toolBar
            // 
            this.toolBar.Buttons.AddRange(new System.Windows.Forms.ToolBarButton[] {
            this.toolBarBtnTune,
            this.toolBarBtnGrab,
            this.toolBarBtnSep,
            this.toolBarBtnSave});
            this.toolBar.Cursor = System.Windows.Forms.Cursors.Hand;
            this.toolBar.DropDownArrows = true;
            this.toolBar.ImageList = this.imgListToolBar;
            this.toolBar.Location = new System.Drawing.Point(0, 0);
            this.toolBar.Name = "toolBar";
            this.toolBar.ShowToolTips = true;
            this.toolBar.Size = new System.Drawing.Size(672, 42);
            this.toolBar.TabIndex = 0;
            this.toolBar.ButtonClick += new System.Windows.Forms.ToolBarButtonClickEventHandler(this.toolBar_ButtonClick);
            // 
            // toolBarBtnTune
            // 
            this.toolBarBtnTune.Enabled = false;
            this.toolBarBtnTune.ImageIndex = 0;
            this.toolBarBtnTune.Name = "toolBarBtnTune";
            this.toolBarBtnTune.Text = "Tune";
            this.toolBarBtnTune.ToolTipText = "TV tuner dialog";
            // 
            // toolBarBtnGrab
            // 
            this.toolBarBtnGrab.ImageIndex = 1;
            this.toolBarBtnGrab.Name = "toolBarBtnGrab";
            this.toolBarBtnGrab.Text = "Start capture";
            this.toolBarBtnGrab.ToolTipText = "Grab picture from stream";
            // 
            // toolBarBtnSep
            // 
            this.toolBarBtnSep.Enabled = false;
            this.toolBarBtnSep.Name = "toolBarBtnSep";
            this.toolBarBtnSep.Style = System.Windows.Forms.ToolBarButtonStyle.Separator;
            // 
            // toolBarBtnSave
            // 
            this.toolBarBtnSave.Enabled = false;
            this.toolBarBtnSave.ImageIndex = 2;
            this.toolBarBtnSave.Name = "toolBarBtnSave";
            this.toolBarBtnSave.Text = "Save";
            this.toolBarBtnSave.ToolTipText = "Save image to file";
            // 
            // imgListToolBar
            // 
            this.imgListToolBar.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("imgListToolBar.ImageStream")));
            this.imgListToolBar.TransparentColor = System.Drawing.Color.Transparent;
            this.imgListToolBar.Images.SetKeyName(0, "");
            this.imgListToolBar.Images.SetKeyName(1, "");
            this.imgListToolBar.Images.SetKeyName(2, "");
            // 
            // videoPanel
            // 
            this.videoPanel.BackColor = System.Drawing.Color.Transparent;
            this.videoPanel.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.videoPanel.Dock = System.Windows.Forms.DockStyle.Left;
            this.videoPanel.Location = new System.Drawing.Point(0, 42);
            this.videoPanel.Name = "videoPanel";
            this.videoPanel.Size = new System.Drawing.Size(328, 331);
            this.videoPanel.TabIndex = 1;
            this.videoPanel.Resize += new System.EventHandler(this.videoPanel_Resize);
            // 
            // splitter1
            // 
            this.splitter1.Location = new System.Drawing.Point(328, 42);
            this.splitter1.Name = "splitter1";
            this.splitter1.Size = new System.Drawing.Size(5, 331);
            this.splitter1.TabIndex = 2;
            this.splitter1.TabStop = false;
            // 
            // stillPanel
            // 
            this.stillPanel.AutoScroll = true;
            this.stillPanel.AutoScrollMargin = new System.Drawing.Size(8, 8);
            this.stillPanel.AutoScrollMinSize = new System.Drawing.Size(32, 32);
            this.stillPanel.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.stillPanel.Controls.Add(this.fps_counter);
            this.stillPanel.Controls.Add(this.pictureBox);
            this.stillPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.stillPanel.Location = new System.Drawing.Point(333, 42);
            this.stillPanel.Name = "stillPanel";
            this.stillPanel.Size = new System.Drawing.Size(339, 331);
            this.stillPanel.TabIndex = 3;
            // 
            // fps_counter
            // 
            this.fps_counter.AutoSize = true;
            this.fps_counter.Location = new System.Drawing.Point(5, 8);
            this.fps_counter.Name = "fps_counter";
            this.fps_counter.Size = new System.Drawing.Size(30, 13);
            this.fps_counter.TabIndex = 4;
            this.fps_counter.Text = "FPS:";
            // 
            // pictureBox
            // 
            this.pictureBox.Location = new System.Drawing.Point(8, 8);
            this.pictureBox.Name = "pictureBox";
            this.pictureBox.Size = new System.Drawing.Size(240, 232);
            this.pictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.AutoSize;
            this.pictureBox.TabIndex = 0;
            this.pictureBox.TabStop = false;
            // 
            // resolutionList
            // 
            this.resolutionList.FormattingEnabled = true;
            this.resolutionList.Location = new System.Drawing.Point(522, 12);
            this.resolutionList.Name = "resolutionList";
            this.resolutionList.Size = new System.Drawing.Size(138, 21);
            this.resolutionList.TabIndex = 4;
            this.resolutionList.SelectedIndexChanged += new System.EventHandler(this.resolutionList_SelectedIndexChanged);
            // 
            // MainForm
            // 
            this.AutoScaleBaseSize = new System.Drawing.Size(5, 13);
            this.ClientSize = new System.Drawing.Size(672, 373);
            this.Controls.Add(this.resolutionList);
            this.Controls.Add(this.stillPanel);
            this.Controls.Add(this.splitter1);
            this.Controls.Add(this.videoPanel);
            this.Controls.Add(this.toolBar);
            this.Name = "MainForm";
            this.Text = "Sample Grabber for .NET";
            this.Activated += new System.EventHandler(this.MainForm_Activated);
            this.Closing += new System.ComponentModel.CancelEventHandler(this.MainForm_Closing);
            this.stillPanel.ResumeLayout(false);
            this.stillPanel.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

		}
		#endregion

	/// <summary>
	/// The main entry point for the application.
	/// </summary>
	[STAThread]
	static void Main() 
	{
		Application.Run(new MainForm());
	}

	private void MainForm_Closing(object sender, System.ComponentModel.CancelEventArgs e)
	{
		this.Hide();
		CloseInterfaces();
	}

		/// <summary> detect first form appearance, start grabber. </summary>
		private void MainForm_Activated(object sender, System.EventArgs e)
		{
			if (firstActive)
				return;
			firstActive = true;

			if (!DsUtils.IsCorrectDirectXVersion())
			{
				MessageBox.Show(this, "DirectX 8.1 NOT installed!", "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop);
				this.Close(); return;
			}

			if (!DsDev.GetDevicesOfCat(FilterCategory.VideoInputDevice, out capDevices))
			{
				MessageBox.Show(this, "No video capture devices found!", "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop);
				this.Close(); return;
			}

			DsDevice dev = null;
			if (capDevices.Count == 1)
			{
				dev = capDevices[0] as DsDevice;
				videoDevice = 0;
			}
			else
			{
				DeviceSelector selector = new DeviceSelector(capDevices);
				selector.ShowDialog(this);
				dev = selector.SelectedDevice;
                videoDevice = capDevices.IndexOf(selector.SelectedDevice);
            }

			if (dev == null)
			{
				this.Close(); return;
			}

			if (!StartupVideo(dev.Mon))
				this.Close();

            resolutionList.SelectedIndex = videoMode;
            resListInit = true;
        }

		private void videoPanel_Resize(object sender, System.EventArgs e)
		{
			ResizeVideoWindow();
		}


		/// <summary> handler for toolbar button clicks. </summary>
		private void toolBar_ButtonClick(object sender, System.Windows.Forms.ToolBarButtonClickEventArgs e)
		{
			Trace.WriteLine("!!BTN: toolBar_ButtonClick");

			int hr;
			if (sampGrabber == null)
				return;

			if (e.Button == toolBarBtnGrab)
			{
				//Trace.WriteLine( "!!BTN: toolBarBtnGrab" );

				if (!capturing)
				{
					if (savedArray == null)
					{
						int size = videoInfoHeader.BmiHeader.ImageSize;
						if ((size < 1000) || (size > 16000000))
							return;
						savedArray = new byte[size + 64000];
					}

					/*toolBarBtnSave.Enabled = false;
					Image old = pictureBox.Image;
					pictureBox.Image = null;
					if( old != null )
						old.Dispose();

					toolBarBtnGrab.Enabled = false;
					captured = false;*/
					toolBarBtnGrab.Text = "End capture";
					capturing = true;
					hr = sampGrabber.SetCallback(this, 1);
				}
				else
				{
					toolBarBtnGrab.Text = "Start capture";
					capturing = false;
					hr = sampGrabber.SetCallback(null, 0);
				}
			}
			else if (e.Button == toolBarBtnSave)
			{
				Trace.WriteLine("!!BTN: toolBarBtnSave");

				SaveFileDialog sd = new SaveFileDialog();
				sd.FileName = @"DsNET.bmp";
				sd.Title = "Save Image as...";
				sd.Filter = "Bitmap file (*.bmp)|*.bmp";
				sd.FilterIndex = 1;
				if (sd.ShowDialog() != DialogResult.OK)
					return;

				pictureBox.Image.Save(sd.FileName, ImageFormat.Bmp);        // save to new bmp file
			}
			else if (e.Button == toolBarBtnTune)
			{
				if (capGraph != null)
					DsUtils.ShowTunerPinDialog(capGraph, capFilter, this.Handle);
			}

		}

		private bool capturing = false;
		private long frameCount = 0;
		private Mutex frameCaptureMtx = new Mutex();
		/// <summary> capture event, triggered by buffer callback. </summary>
		void OnCaptureDone(byte[] bytes)
		{
			//fps_counter.Text = "FPS: " + FPS;
			Trace.WriteLine("!!DLG: OnCaptureDone");
			if (!capturing)
			{
				sampGrabber.SetCallback(null, 0);
				return;
			}
			try {

				//toolBarBtnGrab.Enabled = true;
				int hr;
				if (sampGrabber == null)
					return;
				//hr = sampGrabber.SetCallback( null, 0 );

				int w = videoInfoHeader.BmiHeader.Width;
				int h = videoInfoHeader.BmiHeader.Height;
				if (((w & 0x03) != 0) || (w < 32) || (w > 4096) || (h < 32) || (h > 4096))
					return;
				int stride = w * 3;

				GCHandle handle = GCHandle.Alloc(bytes, GCHandleType.Pinned);
				long scan0 = (long)handle.AddrOfPinnedObject();     //zmiana z inta na longa aby uniknac OverflowException
				scan0 += (h - 1) * stride;
				Bitmap b = new Bitmap(w, h, -stride, PixelFormat.Format24bppRgb, (IntPtr)scan0);

				b.Save($"frame{frameCount}.jpg");
				b.Save($"frame{frameCount++}.bmp");
				Trace.WriteLine($"Saved frame {frameCount - 1}");

				handle.Free();
				/*savedArray = null;
				Image old = pictureBox.Image;
				pictureBox.Image = b;
				if( old != null )
					old.Dispose();
				toolBarBtnSave.Enabled = true;*/
			}
			catch (Exception ee)
			{
				MessageBox.Show(this, "Could not grab picture\r\n" + ee.Message, "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop);
			}
		}



		/// <summary> start all the interfaces, graphs and preview window. </summary>
	bool StartupVideo( UCOMIMoniker mon )
	{
		int hr;
		try {
			if( ! CreateCaptureDevice( mon ) )
				return false;

			if( ! GetInterfaces() )
				return false;

			if( ! SetupGraph() )
				return false;

			if( ! SetupVideoWindow() )
				return false;

			#if DEBUG
				DsROT.AddGraphToRot( graphBuilder, out rotCookie );		// graphBuilder capGraph
			#endif
			
			hr = mediaCtrl.Run();
			if( hr < 0 )
				Marshal.ThrowExceptionForHR( hr );

			bool hasTuner = DsUtils.ShowTunerPinDialog( capGraph, capFilter, this.Handle );
			toolBarBtnTune.Enabled = hasTuner;

			return true;
		}
		catch( Exception ee )
		{
			MessageBox.Show( this, "Could not start video stream\r\n" + ee.Message, "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop );
			return false;
		}
	}

		/// <summary> make the video preview window to show in videoPanel. </summary>
	bool SetupVideoWindow()
	{
		int hr;
		try {
			// Set the video window to be a child of the main window
			hr = videoWin.put_Owner( videoPanel.Handle );
			if( hr < 0 )
				Marshal.ThrowExceptionForHR( hr );

			// Set video window style
			hr = videoWin.put_WindowStyle( WS_CHILD | WS_CLIPCHILDREN );
			if( hr < 0 )
				Marshal.ThrowExceptionForHR( hr );

			// Use helper function to position video window in client rect of owner window
			ResizeVideoWindow();

			// Make the video window visible, now that it is properly positioned
			hr = videoWin.put_Visible( DsHlp.OATRUE );
			if( hr < 0 )
				Marshal.ThrowExceptionForHR( hr );

			hr = mediaEvt.SetNotifyWindow( this.Handle, WM_GRAPHNOTIFY, IntPtr.Zero );
			if( hr < 0 )
				Marshal.ThrowExceptionForHR( hr );
			return true;
		}
		catch( Exception ee )
		{
			MessageBox.Show( this, "Could not setup video window\r\n" + ee.Message, "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop );
			return false;
		}
	}


		/// <summary> build the capture graph for grabber. </summary>
		bool SetupGraph()
		{
			int hr;
			try
			{
                Guid streamConfigId = typeof(IAMStreamConfig).GUID;
                object videoConfigObj;

                hr = capGraph.FindInterface(PinCategory.Capture,
                MediaType.Video,
                capFilter, streamConfigId, out videoConfigObj);

                videoConfig = videoConfigObj as IAMStreamConfig;
				videoConfig.GetNumberOfCapabilities(out int pCount, out int pSize);
                mtypes = new AMMediaType[pCount/2];
				
				IntPtr cc = Marshal.AllocCoTaskMem(pSize);
                for (int x = 0; x < pCount; x+=2) {
					
					videoConfig.GetStreamCaps(x, out AMMediaType ppmt, cc);
					mtypes[x/2] = ppmt;
					if (!resListInit)
					{
						VideoInfoHeader tvh = (VideoInfoHeader)Marshal.PtrToStructure(ppmt.formatPtr, typeof(VideoInfoHeader));
						resolutionList.Items.Add(tvh.BmiHeader.Width + "x" + tvh.BmiHeader.Height);
					}
                    
					//Trace.WriteLine(mtypes[x / 2].BmiHeader.Width + "x" + mtypes[x / 2].BmiHeader.Height);
				}

				videoConfig.SetFormat(mtypes[videoMode]);

                hr = capGraph.SetFiltergraph(graphBuilder);
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);

				hr = graphBuilder.AddFilter(capFilter, "Ds.NET Video Capture Device");
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);

				DsUtils.ShowCapPinDialog(capGraph, capFilter, this.Handle);

				AMMediaType media = new AMMediaType();
				media.majorType = MediaType.Video;
				media.subType = MediaSubType.RGB24;
				media.formatType = FormatType.VideoInfo;        // ???
                hr = sampGrabber.SetMediaType(media);
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);

                hr = graphBuilder.AddFilter(baseGrabFlt, "Ds.NET Grabber");
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);


                Guid cat = PinCategory.Preview;
				Guid med = MediaType.Video;
				hr = capGraph.RenderStream(ref cat, ref med, capFilter, null, null); // baseGrabFlt 
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);

				cat = PinCategory.Capture;
				med = MediaType.Video;
				hr = capGraph.RenderStream(ref cat, ref med, capFilter, null, baseGrabFlt); // baseGrabFlt 
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);

				media = new AMMediaType();
				hr = sampGrabber.GetConnectedMediaType(media);
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);
				if ((media.formatType != FormatType.VideoInfo) || (media.formatPtr == IntPtr.Zero))
					throw new NotSupportedException("Unknown Grabber Media Format");

				videoInfoHeader = (VideoInfoHeader)Marshal.PtrToStructure(media.formatPtr, typeof(VideoInfoHeader));
				Marshal.FreeCoTaskMem(media.formatPtr); media.formatPtr = IntPtr.Zero;

				hr = sampGrabber.SetBufferSamples(false);
				if (hr == 0)
					hr = sampGrabber.SetOneShot(false);
				if (hr == 0)
					hr = sampGrabber.SetCallback(null, 0);
				if (hr < 0)
					Marshal.ThrowExceptionForHR(hr);

                return true;
			}
			catch (Exception ee)
			{
				MessageBox.Show(this, "Could not setup graph\r\n" + ee.Message, "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop);
				return false;
			}
		}


		/// <summary> create the used COM components and get the interfaces. </summary>
		bool GetInterfaces()
		{
			Type comType = null;
			object comObj = null;
			try
			{
				comType = Type.GetTypeFromCLSID(Clsid.FilterGraph);
				if (comType == null)
					throw new NotImplementedException(@"DirectShow FilterGraph not installed/registered!");
				comObj = Activator.CreateInstance(comType);
				graphBuilder = (IGraphBuilder)comObj; comObj = null;

				Guid clsid = Clsid.CaptureGraphBuilder2;
				Guid riid = typeof(ICaptureGraphBuilder2).GUID;
				comObj = DsBugWO.CreateDsInstance(ref clsid, ref riid);
				capGraph = (ICaptureGraphBuilder2)comObj; comObj = null;

				comType = Type.GetTypeFromCLSID(Clsid.SampleGrabber);
				if (comType == null)
					throw new NotImplementedException(@"DirectShow SampleGrabber not installed/registered!");
				comObj = Activator.CreateInstance(comType);
				sampGrabber = (ISampleGrabber)comObj; comObj = null;

				mediaCtrl = (IMediaControl)graphBuilder;
				videoWin = (IVideoWindow)graphBuilder;
				mediaEvt = (IMediaEventEx)graphBuilder;
				baseGrabFlt = (IBaseFilter)sampGrabber;
				return true;
			}
			catch (Exception ee)
			{
				MessageBox.Show(this, "Could not get interfaces\r\n" + ee.Message, "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop);
				return false;
			}
			finally
			{
				if (comObj != null)
					Marshal.ReleaseComObject(comObj); comObj = null;
			}
		}

        /// <summary> create the user selected capture device. </summary>
        bool CreateCaptureDevice(UCOMIMoniker mon)
		{
			object capObj = null;
			try
			{
				Guid gbf = typeof(IBaseFilter).GUID;
				mon.BindToObject(null, null, ref gbf, out capObj);
				capFilter = (IBaseFilter)capObj; capObj = null;

                return true;
			}
			catch (Exception ee)
			{
				MessageBox.Show(this, "Could not create capture device\r\n" + ee.Message, "DirectShow.NET", MessageBoxButtons.OK, MessageBoxIcon.Stop);
				return false;
			}
			finally
			{
				if (capObj != null)
					Marshal.ReleaseComObject(capObj); capObj = null;
			}

		}



		/// <summary> do cleanup and release DirectShow. </summary>
		void CloseInterfaces()
		{
			int hr;
			try
			{
#if DEBUG
				if (rotCookie != 0)
					DsROT.RemoveGraphFromRot(ref rotCookie);
#endif

				if (mediaCtrl != null)
				{
					hr = mediaCtrl.Stop();
					mediaCtrl = null;
				}

				if (mediaEvt != null)
				{
					hr = mediaEvt.SetNotifyWindow(IntPtr.Zero, WM_GRAPHNOTIFY, IntPtr.Zero);
					mediaEvt = null;
				}

				if (videoWin != null)
				{
					hr = videoWin.put_Visible(DsHlp.OAFALSE);
					hr = videoWin.put_Owner(IntPtr.Zero);
					videoWin = null;
				}

				baseGrabFlt = null;
				if (sampGrabber != null)
					Marshal.ReleaseComObject(sampGrabber); sampGrabber = null;

				if (capGraph != null)
					Marshal.ReleaseComObject(capGraph); capGraph = null;

				if (graphBuilder != null)
					Marshal.ReleaseComObject(graphBuilder); graphBuilder = null;

				if (capFilter != null)
					Marshal.ReleaseComObject(capFilter); capFilter = null;

				if (capDevices != null)
				{
					foreach (DsDevice d in capDevices)
						d.Dispose();
					capDevices = null;
				}
			}
			catch (Exception)
			{ }
		}

		/// <summary> resize preview video window to fill client area. </summary>
	void ResizeVideoWindow()
	{
		if( videoWin != null )
		{
			Rectangle rc = videoPanel.ClientRectangle;
			videoWin.SetWindowPosition( 0, 0, rc.Right, rc.Bottom );
		}
	}

		/// <summary> override window fn to handle graph events. </summary>
	protected override void WndProc( ref Message m )
	{
		if( m.Msg == WM_GRAPHNOTIFY )
			{
			if( mediaEvt != null )
				OnGraphNotify();
			return;
			}
		base.WndProc( ref m );
	}

		/// <summary> graph event (WM_GRAPHNOTIFY) handler. </summary>
	void OnGraphNotify()
	{
		DsEvCode	code;
		int p1, p2, hr = 0;
		do
		{
			hr = mediaEvt.GetEvent( out code, out p1, out p2, 0 );
			if( hr < 0 )
				break;
			hr = mediaEvt.FreeEventParams( code, p1, p2 );
		}
		while( hr == 0 );
	}

		/// <summary> sample callback, NOT USED. </summary>
	int ISampleGrabberCB.SampleCB( double SampleTime, IMediaSample pSample )
	{
		Trace.WriteLine( "!!CB: ISampleGrabberCB.SampleCB" );
		return 0;
	}

	//potrzebne do implementacji pseudokodu
	private Stopwatch czas = new Stopwatch();
	private long czas_poprzedni = 0;
	private int FPS = 0;
	private long last_cap = -1;

		/// <summary> buffer callback, COULD BE FROM FOREIGN THREAD. </summary>
		int ISampleGrabberCB.BufferCB(double SampleTime, IntPtr pBuffer, int BufferLen)
		{
			//implementacja pseudokodu do pomiaru fps
			bool upd = false;
			int updFPS = 0;
			if (!czas.IsRunning)
			{
				czas.Start();
			} else
			{
				long ile_czasu_uplynelo = czas.ElapsedMilliseconds - czas_poprzedni;

				FPS++;
				if (ile_czasu_uplynelo > 1000)
				{
					czas_poprzedni = czas.ElapsedMilliseconds;
					upd = true;
					Trace.WriteLine(FPS);
					updFPS = FPS;
					FPS = 0;
				}
			}
			if (last_cap + 2 > czas.ElapsedMilliseconds)        //blokujemy do 333 fps aby watek glowny nadazyl
			{
				return 0;
			}
			last_cap = czas.ElapsedMilliseconds;
			/*if( captured || (savedArray == null) )
			{
				//Trace.WriteLine( "!!CB: ISampleGrabberCB.BufferCB" );
				return 0;
			}*/

			captured = true;
			bufferedSize = BufferLen;
			//Trace.WriteLine( "!!CB: ISampleGrabberCB.BufferCB  !GRAB! size = " + BufferLen.ToString() );
			if ((pBuffer != IntPtr.Zero) && (BufferLen > 1000))
			{
				int size = videoInfoHeader.BmiHeader.ImageSize;
				byte[] newBytes = new byte[size + 64000];
				Marshal.Copy(pBuffer, newBytes, 0, BufferLen);
				this.OnCaptureDone(newBytes);
				if (upd)
				{
					this.BeginInvoke(new CaptureDone(delegate
					{

						fps_counter.Text = "FPS: " + updFPS;
						//this.OnCaptureDone(newBytes);
					}));
				}
			}
			else
				Trace.WriteLine("    !!!GRAB! failed ");
			//this.BeginInvoke( new CaptureDone( this.OnCaptureDone ) );

			return 0;
		}

		private void resolutionList_SelectedIndexChanged(object sender, EventArgs e)
        {
			if (!resListInit)
			{
				return;
			}
			//videoConfig.SetFormat(mtypes[]);			
			videoMode = resolutionList.SelectedIndex;
            CloseInterfaces();
			DsDev.GetDevicesOfCat(FilterCategory.VideoInputDevice, out capDevices);
			StartupVideo((capDevices[videoDevice] as DsDevice).Mon);
			//SetupGraph();
        }

		private int videoDevice = 0;
		private int videoMode = 0;

        private AMMediaType[] mtypes;
		private IAMStreamConfig	videoConfig;

		private bool resListInit = false;
        /// <summary> flag to detect first Form appearance </summary>
    private bool					firstActive;

		/// <summary> base filter of the actually used video devices. </summary>
	private IBaseFilter				capFilter;

		/// <summary> graph builder interface. </summary>
	private IGraphBuilder			graphBuilder;

		/// <summary> capture graph builder interface. </summary>
	private ICaptureGraphBuilder2	capGraph;
	private ISampleGrabber			sampGrabber;

		/// <summary> control interface. </summary>
	private IMediaControl			mediaCtrl;

		/// <summary> event interface. </summary>
	private IMediaEventEx			mediaEvt;

		/// <summary> video window interface. </summary>
	private IVideoWindow			videoWin;

		/// <summary> grabber filter interface. </summary>
	private IBaseFilter				baseGrabFlt;

		/// <summary> structure describing the bitmap to grab. </summary>
	private	VideoInfoHeader			videoInfoHeader;
	private	bool					captured = true;
	private	int						bufferedSize;

		/// <summary> buffer for bitmap data. </summary>
	private	byte[]					savedArray;

		/// <summary> list of installed video devices. </summary>
	private ArrayList				capDevices;

	private const int WM_GRAPHNOTIFY	= 0x00008001;	// message from graph

	private const int WS_CHILD			= 0x40000000;	// attributes for video window
	private const int WS_CLIPCHILDREN	= 0x02000000;
	private const int WS_CLIPSIBLINGS	= 0x04000000;

		/// <summary> event when callback has finished (ISampleGrabberCB.BufferCB). </summary>
	private delegate void CaptureDone();

	#if DEBUG
		private int		rotCookie = 0;
 
#endif
    }

    internal enum PlayState
{
	Init, Stopped, Paused, Running
}

}
