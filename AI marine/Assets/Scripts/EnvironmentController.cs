using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnvironmentController : MonoBehaviour
{
    public static bool isControlledByAI = false;
    public static bool isTraining = false;
    public static  List<GameObject> ports = new List<GameObject>();
    public static int randomPorts;
    public static GameObject parent;


    [SerializeField] public static GameObject staticportAsset;
    public GameObject portAsset;
    public GameObject Boat;



    public static float maxZ = 1615f;
    public static float minZ = 173f;
    public static float maxX = 1628f;
    public static float minX = -316f;
    public static float posY = -5.18f;


    public float BoatSpeed;


    Vector3 previousPosition;
    Vector3 currentPosition;

    float time = 0;



    void Awake()
    {
        Screen.fullScreen = false;
        parent = new GameObject();
        parent.name = "Ports";
        if (portAsset != null)
        {
            staticportAsset = portAsset;
        }
        instantiatePorts();
        RandomisePortLocation();

        currentPosition = Boat.transform.position;
        previousPosition = Boat.transform.position;
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
    }


    void FixedUpdate()
    {
        
        
        // This part handels the key mappings 
        if (Input.GetKeyDown(KeyCode.F))
        {
            isControlledByAI = !isControlledByAI;
        }
        if (Input.GetKeyDown(KeyCode.R))
        {
            staticportAsset = portAsset;
            RandomisePortLocation();
        }
        if (Input.GetKeyDown(KeyCode.T))
        {
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

    void  instantiatePorts()
    {
        if (staticportAsset != null)
        {      
            for (int i = 0; i < 15; i++)
            {
                //Vector3 positions = new Vector3(Random.Range(minX, maxX), posY, Random.Range(minZ, maxZ));
                Vector3 positions = new Vector3(0,-820, 0);
                GameObject port = (GameObject)Instantiate(staticportAsset, positions, Quaternion.identity,parent.transform);
                ports.Add(port);
            }
        }
        else {
            Debug.Log("Randomise Ports Failed || Asset not found");
        }

        
    }

    public static void RandomisePortLocation()
    {
        foreach(GameObject port in ports)
        {
            port.transform.position = new Vector3(0, -820, 0);
        }
        randomPorts = Random.Range(8, 15);

        for (int i = 0; i < randomPorts; i++)
        {
            Vector3 positions = new Vector3(Random.Range(minX, maxX), posY, Random.Range(minZ, maxZ));
            ports[i].transform.localPosition = positions;
        }
    }
}
