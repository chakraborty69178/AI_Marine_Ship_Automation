using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIController : MonoBehaviour
{
    public Text isTraining;
    public Text isControlledByAI;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        isTraining.text = "Is Training : " + EnvironmentController.isTraining;
        isControlledByAI.text = "IsControlled By AI : " + EnvironmentController.isControlledByAI;


    }
}
