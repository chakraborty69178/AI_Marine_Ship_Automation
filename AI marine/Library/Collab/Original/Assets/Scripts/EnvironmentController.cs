using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System.IO;
using System.Text;

public class EnvironmentController : MonoBehaviour
{
    public static bool isControlledByAI = false;
    public static bool isTraining = false;
    public static  List<GameObject> ports = new List<GameObject>();
    public static List<GameObject> hurdles = new List<GameObject>();
    public static int randomPorts;
    public static int randomHurdles;
    public static GameObject parent;
    public static GameObject hurdleParent;


    public static GameObject staticportAsset;
    public static GameObject staticHurdleAsset;
    public GameObject portAsset;
    public GameObject Boat;
    public GameObject hurdleAsset;
   



    public static float maxZ = 1615f;
    public static float minZ = 173f;
    public static float maxX = 1628f;
    public static float minX = -316f;
    public static float posY = -5.18f;

    string portsCoOrdinateFile = "";
    string trainingDatasetFile = "";
    string leftCamData = "";
    string rightCamData = "";
    string midCamData = "";
    string shipCoOrdinateFile = "";


    public float BoatSpeed;


    Vector3 previousPosition;
    Vector3 currentPosition;
    float time = 0;

    public Camera leftCam;
    public Camera midCam;
    public Camera rightCam;
    int resWidth = 320;
    int resHeight = 240;
    StringBuilder trainingDataSet;
    int Fname;
    float frameCounter = 0;
    float shipLocationframeCounter = 0;
    public int locationCaptureInterval = 1470000;
    public int sreenshotInterval = 1470000;


    void Awake()
    {
        //GenerateShipLocationFile();
        // Initialise all file path name here
        //portsCoOrdinateFile = Application.dataPath + "/AIdata/dataset/PortsCoordinates.csv";
        //trainingDatasetFile = Application.dataPath + "/AIdata/dataset/dataset.csv";
        //leftCamData = Application.dataPath + "/AIdata/dataset/Left/";
        // midCamData = Application.dataPath + "/AIdata/dataset/Mid/";
        //rightCamData = Application.dataPath + "/AIdata/dataset/Right/";

        portsCoOrdinateFile = "D:/AI_Marine_Ship_Automation/AIdata/dataset/PortsCoordinates.csv";
        shipCoOrdinateFile = "D:/AI_Marine_Ship_Automation/AIdata/dataset/shipCoordinate.csv";
        trainingDatasetFile = "D:/AI_Marine_Ship_Automation/AIdata/dataset/dataset.csv";
        leftCamData = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Left/";
        midCamData = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Mid/";
        rightCamData = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Right/";

        leftCam.gameObject.SetActive(false);
        midCam.gameObject.SetActive(false);
        rightCam.gameObject.SetActive(false);


        //initialise micelinous variables

        Screen.fullScreen = false;
        parent = new GameObject();
        hurdleParent = new GameObject();
        parent.name = "Ports";
        if (portAsset != null)
        {
            staticportAsset = portAsset;
        }
        if (hurdleAsset != null)
        {
            staticHurdleAsset = hurdleAsset;
        }


        //initiate Ports Location and Export file

        instantiatePorts();
        RandomisePortLocation();
        GeneratePortFile();
        GenerateShipLocationFile();

        currentPosition = Boat.transform.position;
        previousPosition = Boat.transform.position;


        // Initialise Camera Render texture for screenshots
        if (leftCam.targetTexture == null)
        {
            leftCam.targetTexture = new RenderTexture(resWidth, resHeight, 24);
        }
        if (midCam.targetTexture == null)
        {
            midCam.targetTexture = new RenderTexture(resWidth, resHeight, 24);
        }
        if (rightCam.targetTexture == null)
        {
            rightCam.targetTexture = new RenderTexture(resWidth, resHeight, 24);
        }
        
    }

    

    public void Update()
    {
        // This part calculates boat speed through velocity in rigidBody
        currentPosition = Boat.transform.position;
        time += Time.deltaTime;
        float calcDistance = Mathf.Sqrt(Mathf.Pow(currentPosition.x - previousPosition.x ,2) + Mathf.Pow(currentPosition.z - previousPosition.z , 2));
        //Debug.Log(calcDistance);
        BoatSpeed = calcDistance / time;
        time = 0;
        previousPosition = currentPosition;
        //Debug.Log(BoatSpeed);


        // This part handels the key mappings 
        if (Input.GetKeyDown(KeyCode.F))
        {
            isControlledByAI = !isControlledByAI;
        }
        if (Input.GetKeyDown(KeyCode.R))
        {
            staticportAsset = portAsset;
            RandomisePortLocation();
            GeneratePortFile();
            GenerateShipLocationFile();// Generate new port data
        }


        if (Input.GetKeyDown(KeyCode.T))
        {
            if (!isTraining)
            {
                //Fname = 0;
                trainingDataSet = new StringBuilder();
                trainingDataSet.Append("LeftPath,MidPath,RightPath,Speed,KeyOutput\n");
            }
            else
            {
                //Fname = 0;
                
                GenerateDataset();
                trainingDataSet = new StringBuilder();
            }
            isTraining = !isTraining;

        }
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Application.Quit();
        }
        if (Input.GetKeyDown(KeyCode.Z))
        {
            Screen.fullScreen = !Screen.fullScreen;
        }



        
    }


    void FixedUpdate()
    {
        
        // Taking Screenshot Everyframe
        
    }

    private void LateUpdate()
    {
        if (isTraining)
        {
            frameCounter += Time.deltaTime;
            shipLocationframeCounter += Time.deltaTime;
            CallTakeSnapshot();
            if (shipLocationframeCounter >= locationCaptureInterval)
            {
                shipLocationframeCounter = 0;
                GenerateShipLocationFile();
            }

        }
    }


    // Generate Screenshots and Training Dataset
    private void CallTakeSnapshot()
    {
       
           
            leftCam.gameObject.SetActive(true);
            midCam.gameObject.SetActive(true);
            rightCam.gameObject.SetActive(true);
            if (leftCam.gameObject.activeSelf && midCam.gameObject.activeSelf && rightCam.gameObject.activeSelf)
            {
                Texture2D snapshot = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
                leftCam.Render();
                RenderTexture.active = leftCam.targetTexture;
                snapshot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
                byte[] leftCamByte = snapshot.EncodeToPNG();
                string leftname = leftCamData + "Left_" + Fname + ".png";
                

                midCam.Render();
                RenderTexture.active = midCam.targetTexture;
                snapshot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
                byte[] midCamByte = snapshot.EncodeToPNG();
                string midname = midCamData + "Mid_" + Fname + ".png";
               
                rightCam.Render();
                RenderTexture.active = rightCam.targetTexture;
                snapshot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
                byte[] rightCamByte = snapshot.EncodeToPNG();
                string rightname = rightCamData + "Right_" + Fname + ".png";

            if (frameCounter >= sreenshotInterval)
            {
               
                frameCounter = 0;
                System.IO.File.WriteAllBytes(leftname, leftCamByte);
                System.IO.File.WriteAllBytes(midname, midCamByte);
                System.IO.File.WriteAllBytes(rightname, rightCamByte);
                Debug.Log("Executed");
            }
            string keyMap = "";

            if (Input.GetKey(KeyCode.LeftArrow) && Input.GetKey(KeyCode.UpArrow))
            {
                keyMap = "Left|Up";

            }
            else if (Input.GetKey(KeyCode.RightArrow) && Input.GetKey(KeyCode.UpArrow))
            {
                keyMap = "Right|Up";

            }
            else if (Input.GetKey(KeyCode.LeftArrow) && Input.GetKey(KeyCode.DownArrow))
            {
                keyMap = "Left|Down";

            }
            else if (Input.GetKey(KeyCode.RightArrow) && Input.GetKey(KeyCode.DownArrow))
            {
                keyMap = "Right|Down";

            }

            else if (Input.GetKey(KeyCode.UpArrow))
            {
                keyMap = "Up";
            }
            else if (Input.GetKey(KeyCode.DownArrow))
            {
                keyMap = "Down";

            }
            else if (Input.GetKey(KeyCode.RightArrow))
            {
                keyMap = "Right";

            }
            else if (Input.GetKey(KeyCode.LeftArrow))
            {
                keyMap = "Left";

            }
            else {

                keyMap = "NULL";
            }

            Debug.Log(keyMap);
            trainingDataSet.Append(leftname + "," + midname + "," + rightname + "," + BoatSpeed + "," + keyMap + "\n");

                Fname = Fname + 1;
            }
            leftCam.gameObject.SetActive(false);
            midCam.gameObject.SetActive(false);
            rightCam.gameObject.SetActive(false);
        
    }

private void instantiatePorts()
{
    if (staticportAsset != null)
    {
        for (int i = 0; i < 15; i++)
        {
            //Vector3 positions = new Vector3(Random.Range(minX, maxX), posY, Random.Range(minZ, maxZ));
            Vector3 positions = new Vector3(0, -820, 0);
            GameObject port = (GameObject)Instantiate(staticportAsset, positions, Quaternion.identity, parent.transform);
            ports.Add(port);
        }
    }
    else
    {
        Debug.Log("Randomise Ports Failed || Asset not found");
    }

    if (staticHurdleAsset != null)
    {
        for (int i = 0; i < 1000; i++)
        {
                //Vector3 positions = new Vector3(Random.Range(minX, maxX), posY, Random.Range(minZ, maxZ));
                Vector3 positions = new Vector3(0, -820, 0);
                GameObject hurdle = (GameObject)Instantiate(staticHurdleAsset, positions, Quaternion.identity, hurdleParent.transform);
                hurdles.Add(hurdle);
        }
    }
    else
    {
        Debug.Log("Randomise Ports Failed || Asset not found");
    }


    }

public static void RandomisePortLocation()
    {
        foreach(GameObject port in ports)
        {
            port.transform.position = new Vector3(0, -820, 0);
        }
        randomPorts = Random.Range(10, 15);

        for (int i = 0; i < randomPorts; i++)
        {
            Vector3 positions = new Vector3(Random.Range(minX, maxX), posY, Random.Range(minZ, maxZ));
            ports[i].transform.localPosition = positions;
        }

        foreach (GameObject hurdle in hurdles)
        {
            hurdle.transform.position = new Vector3(0, -820, 0);
        }
        randomHurdles = Random.Range(900, 1000);

        for (int i = 0; i < randomHurdles; i++)
        {
            Vector3 positions = new Vector3(Random.Range(minX, maxX), posY, Random.Range(minZ, maxZ));
            hurdles[i].transform.localPosition = positions;
        }
    }


    // Function Creates Ports Cordinate file
    public  void GeneratePortFile()
    { 
        if(ports.ToArray().Length > 0)
        {
            TextWriter tw = new StreamWriter(portsCoOrdinateFile, false);
            tw.WriteLine("S.No,Coordinates(X||Z)");
            tw.Close();

            tw = new StreamWriter(portsCoOrdinateFile, true);
            for (int i = 0; i < randomPorts; i++)
            {
                float X = ports[i].transform.localPosition.x;
                float Z = ports[i].transform.localPosition.z;

                tw.WriteLine((i+1)+","+X+"||"+Z);
                
            }
            tw.Close();

            Debug.Log("Check Path: "+portsCoOrdinateFile);

        }
        else
        {
            Debug.LogError("Nothing to write");
        }
    }

    public void GenerateShipLocationFile()
    {
        Debug.Log("Ship Location 1");
        if (Boat != null)
        {
            float shipX = Boat.transform.position.x;
            float shipZ = Boat.transform.position.z;
            Debug.Log("Ship Location 1.1");
            TextWriter tw = new StreamWriter(shipCoOrdinateFile, false);
            tw.WriteLine("Coordinates(X||Z),");
            tw.WriteLine(shipX + "||" + shipZ);
            tw.Close();
            
            
            

            Debug.Log("Check Path: " + shipCoOrdinateFile);

        }
        else
        {
            Debug.LogError("Nothing to write");
        }
    }

    void GenerateDataset()
    {
        if (trainingDataSet != null)
        {
            TextWriter tw = new StreamWriter(trainingDatasetFile, false);
            tw.Write(trainingDataSet);
            tw.Close();

        }
    }

   
}
