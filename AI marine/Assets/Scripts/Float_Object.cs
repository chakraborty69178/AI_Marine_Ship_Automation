using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Float_Object : MonoBehaviour
{
    // Start is called before the first frame update
    public float waterLevel = 0;
    public float floatThreshold = 2f;
    public float waterDencity = 0.125f;
    public float downForce = 4f;

    float forceFactor;
    Vector3 floatForce;

    void Start()
    {
        
    }

    void FixedUpdate()
    {
        forceFactor = 1.0f - ((transform.position.y - waterLevel) / floatThreshold);

        if (forceFactor > 0.0f)
        {
            floatForce = -Physics.gravity * GetComponent<Rigidbody>().mass *(forceFactor - GetComponent<Rigidbody>().velocity.y * waterDencity);
            floatForce += new Vector3(0.0f, -downForce * GetComponent<Rigidbody>().mass , 0.0f);
            GetComponent<Rigidbody>().AddForceAtPosition(floatForce, transform.position);
        }
    }
}
