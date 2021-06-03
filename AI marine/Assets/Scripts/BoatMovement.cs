using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoatMovement : MonoBehaviour
{

    [SerializeField] float trust;
    [SerializeField] float turningSpeed;

    public Vector3 COM;
    [Space(15)]
    public float speed = 1.0f;
    public float steerSpeed = 1.0f;
    public float movementThresold = 10.0f;

    Transform m_COM;
    float verticalInput;
    float movementFactor;
    float horizontalInput;
    float steerFactor;

    float Volume;
    const float pH2O = 1000;

    Rigidbody rb;
    BoxCollider box;


    void Start()
    {
        rb = GetComponent<Rigidbody>();
        box = GetComponent<BoxCollider>();
    }
    void Balance()
    {
        if (!m_COM)
        {
            m_COM = new GameObject("COM").transform;
            m_COM.SetParent(transform);
        }

        m_COM.position = COM;
        GetComponent<Rigidbody>().centerOfMass = m_COM.position;
    }

    void Movement()
    {
       
            verticalInput = Input.GetAxis("Vertical");
            movementFactor = Mathf.Lerp(movementFactor, verticalInput, Time.deltaTime / movementThresold);
            transform.Translate(0.0f, 0.0f, movementFactor * speed);
            //rb.AddRelativeForce(Vector3.forward * trust * Time.fixedDeltaTime * Input.GetAxis("Vertical"));
    }

    void FixedUpdate()
    {
        if (Input.GetAxis("Horizontal") < -.4f || Input.GetAxis("Horizontal") > .4f)
        {
            transform.rotation = Quaternion.EulerRotation(0, transform.rotation.ToEulerAngles().y + Input.GetAxis("Horizontal") * turningSpeed * Time.fixedDeltaTime, 0);
        }
        //if (Input.GetAxis("Throttle") > 0.2f)
        //{
        // rb.AddRelativeForce(Vector3.right * trust * Time.fixedDeltaTime * Input.GetAxis("Throttle"));
        // }

        Movement();

    }
}